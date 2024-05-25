from django.contrib import admin
from api.models import CoinInfo, Configurations, Portofolio


class PortofolioAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        Return a QuerySet of all items where in_hold is True or the id is 1.
        """
        qs = super().get_queryset(request)
        return qs.filter(in_hold=True) | qs.filter(id=1)


# Register your models here.
admin.site.register(CoinInfo)
admin.site.register(Configurations)
admin.site.register(Portofolio, PortofolioAdmin)
