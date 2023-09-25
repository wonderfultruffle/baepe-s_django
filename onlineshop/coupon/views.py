from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import AddCouponForm

# Create your views here.
@require_POST
def add_coupon(request):
    now = timezone.now()
    form = AddCouponForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data["code"]

        try:
            coupon = Coupon.objects.get(code__iexact=code, use_from__lte=now, use_to__gte=now, active=True)
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
            # 쿠폰이 사용 불가능한 상태일 때 알려주는 기능 + ui 추가하면 어떨까?

    return redirect("cart:detail")