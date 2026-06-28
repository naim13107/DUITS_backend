from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 1. Imports
from users.views import CustomUserViewSet  # Ensure this is imported
from article.views import CategoryViewSet, ArticleViewSet
from event.views import EventViewSet
from gallery.views import GalleryImageViewSet
from panel.views import PanelMemberViewSet
from recruitment.views import RecruitmentSettingsViewSet, RecruitmentApplicationViewSet
from analytics.views import SystemLogViewSet
from contact.views import ContactMessageViewSet
from payment.views import PaymentViewSet, TransactionViewSet
from notice.views import NoticeViewSet 

# 2. Router Setup
router = DefaultRouter()

# Register ViewSets
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'events', EventViewSet, basename='event')
router.register(r'gallery', GalleryImageViewSet, basename='gallery')
router.register(r'panel-members', PanelMemberViewSet, basename='panelmember')
router.register(r'recruitment-settings', RecruitmentSettingsViewSet, basename='recruitmentsettings')
router.register(r'recruitment-applications', RecruitmentApplicationViewSet, basename='recruitmentapplication')
router.register(r'payment', PaymentViewSet, basename='payment')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'notices', NoticeViewSet, basename='notice')
router.register(r'contact', ContactMessageViewSet, basename='contactmessage')
router.register(r'logs', SystemLogViewSet, basename='systemlog')

# 3. Define Custom User Views (Manual Mapping)
# This maps the Djoser UserViewSet methods to your CustomUserViewSet
user_detail = CustomUserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy' 
})

# 4. URL Patterns
urlpatterns = [
    # Manually map the auth users routes BEFORE the router
    path('auth/users/<int:pk>/', user_detail, name='user-detail'),
    
    # Include standard Djoser auth (token creation, me, etc)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    # Include the rest of your router viewsets
    path('', include(router.urls)),
]