from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from tarifs.services.cinetpay import cinetpaty_notify
from tarifs.services.cinetpay import init_cinetpay


class CinetPayInitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        error_response, result = init_cinetpay(order_id=order_id, user=request.user)
        if error_response:
            return Response(
                {"detail": error_response["detail"]}, status=error_response["status"]
            )
        return Response(result)


class CinetPayNotifyView(APIView):
    permission_classes = []

    def post(self, request):
        cpm_trans_id = request.data.get("cpm_trans_id")
        cpm_site_id = request.data.get("cpm_site_id")
        error_response, success_response = cinetpaty_notify(
            cpm_trans_id=cpm_trans_id, cpm_site_id=cpm_site_id
        )
        if error_response:
            return Response(
                {"detail": error_response["detail"]}, status=error_response["status"]
            )
        return Response(
            {"detail": success_response["detail"]}, status=success_response["status"]
        )
