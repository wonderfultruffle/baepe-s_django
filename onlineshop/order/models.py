import hashlib

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from coupon.models import Coupon
from shop.models import Product
from .iamport import payments_prepare, find_transaction

# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name="order_coupon", null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_product(self):
        return sum(item.get_item_price() for item in self.items.all())

    def get_total_price(self):
        total_product = self.get_total_product()
        return total_product - self.discount

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_products")

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id}"

    def get_item_price(self):
        return self.price * self.quantity


class OrderTransactionManager(models.Manager):
    def create_new(self, order, amount, success=None, transaction_status=None):
        if order is None:
            raise ("주문 오류")

        order_hash = hashlib.sha1(f"{order.id}".encode("utf-8")).hexdigiest()
        email_hash = f"{order.email}".split('@')[0]
        final_hash = hashlib.sha1((order_hash + email_hash).encode("utf-8")).hexdigiest()[:10]
        merchant_order_id = f"{final_hash}"

        payments_prepare(merchant_order_id, amount)

        transaction = self.model(
            order=order,
            merchant_order_id=merchant_order_id,
            amount=amount
        )

        if success is not None:
            transaction.success = success
            transaction.transaction_status = transaction_status

        try:
            transaction.save()
        except Exception as e:
            print("save error ", e)

        return transaction.merchant_order_id

    def get_transaction(self, merchant_order_id):
        result = find_transaction(order_id=merchant_order_id)
        if result["status"] == "paid":
            return result
        else:
            return None

class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)

    amount = models.PositiveIntegerField(default=0)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    type = models.CharField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = OrderTransactionManager() # 처음보는 방식... 기본 objects가 아니라 외부함수를 사용하기 위해 별도의 objects를 지정...

    def __str__(self):
        return f"{self.order.id}"

    class Meta:
        ordering = ["-created"]

# 결제 검증 과정 이해 안됨. sender와 created는 언제 사용되는지...?
def order_payment_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        import_trasaction = OrderTransaction.objects.get_transaction(merchant_order_id=instance.merchant_order_id)

        imp_id = import_trasaction["imp_id"]
        merchant_order_id = import_trasaction["merchant_order_id"]
        amount = import_trasaction["amount"]

        local_transaction = OrderTransaction.objects.filter(merchant_order_id=merchant_order_id, transaction_id=imp_id, amount=amount).exists()

        if not import_trasaction or not local_transaction:
            raise("비정상 거래입니다.")

# 시그널 동작 원리... 잘 모르겠으.ㅁ
from django.db.models.signals import post_save
post_save.connect(order_payment_validation, sender=OrderTransaction) # instance와 created는 어떻게 전달하는지?
