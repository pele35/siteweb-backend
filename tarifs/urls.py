from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from tarifs.api.auth import CustomTokenObtainPairView
from tarifs.api.auth import LogoutView
from tarifs.api.auth import RegisterView
from tarifs.api.auth import SendVerificationCodeView
from tarifs.api.auth import UserProfileView
from tarifs.api.auth import VerifyCodeView
from tarifs.api.cart import CartAddItemView
from tarifs.api.cart import CartRemoveItemView
from tarifs.api.cart import CartSyncView
from tarifs.api.cart import CartUpdateItemView
from tarifs.api.cart import CartView
from tarifs.api.cart import CheckoutView
from tarifs.api.offer import OfferCategoryViewSet
from tarifs.api.offer import OfferListView
from tarifs.api.offer import OfferOptionViewSet
from tarifs.api.offer import PlacementViewSet
from tarifs.api.payment import CinetPayInitView
from tarifs.api.payment import CinetPayNotifyView

router = DefaultRouter()
router.register(r"categories", OfferCategoryViewSet)
router.register(r"options", OfferOptionViewSet)
router.register(r"placements", PlacementViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("offers/", OfferListView.as_view(), name="offer-list"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", CartAddItemView.as_view(), name="cart_add"),
    path("cart/item/<int:item_id>/", CartUpdateItemView.as_view(), name="cart_update"),
    path(
        "cart/item/<int:item_id>/remove/",
        CartRemoveItemView.as_view(),
        name="cart_remove",
    ),
    path("cart/sync/", CartSyncView.as_view(), name="cart_sync"),
    path("order/send-code/", SendVerificationCodeView.as_view()),
    path("order/verify-code/", VerifyCodeView.as_view()),
    path("cinetpay/init/", CinetPayInitView.as_view()),
    path("cinetpay/notify/", CinetPayNotifyView.as_view()),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
