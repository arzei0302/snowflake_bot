from rest_framework.routers import DefaultRouter as DR
from projects.views import ProjectView, UserAppealView


router = DR()
router.register('projects', ProjectView)
router.register('userappeal', UserAppealView)


urlpatterns = []

urlpatterns += router.urls