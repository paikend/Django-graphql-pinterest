from django.db import models
from accounts.models import User
from config.storage_backends import PrivateMediaStorage

# Create your models here.

class Board(models.Model):
    name = models.CharField(
        help_text="Board의 이름입니다.",
        max_length=100, blank=True, null=True)
    user = models.ManyToManyField(User,
        related_name='user',
        help_text="보드의 참여자입니다.",)
    description = models.CharField(
        help_text="보드의 설명입니다.",
        max_length=500, blank=True, null=True)
    subject = models.CharField(
        help_text="보드의 주제입니다.",
        max_length=100, blank=True, null=True)
    
    is_inspired = models.BooleanField(
        help_text="보드의 영감 공개 여부입니다..",
        default=False)
    is_save = models.BooleanField(
        help_text="보드의 저장여부입니다.",
        default=False)
    is_private = models.BooleanField(
        help_text="보드의 공개여부입니다.",
        default=False)
    
    section = models.ManyToManyField('Pin',
        related_name='section',
        help_text="보드의 섹션입니다.",
        through='Section', blank=True, null=True)
    order_key = models.IntegerField(
        help_text="보드의 사용자 정렬입니다.", 
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    def save(self): 
      board_obj = Board.objects.order_by('order_key').first()
      self.order_key = 0
      if board_obj:
        self.order_key = board_obj.order_key + 1
      super(Board, self).save()

class Pin(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    related_link = models.TextField(blank=True, null=True)
    photo = models.ImageField(
    verbose_name='photo (주요 프로필 사진)',
    help_text='크리덴셜과 연결된 주요 프로필 사진입니다.',
    max_length=200,
    blank=True,
    upload_to='pins/%Y/%m/%d',
    storage=PrivateMediaStorage(),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Section(models.Model):
    name = models.CharField(
        help_text="섹션의 이름입니다.",
        max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)    
    board = models.ForeignKey(Board, related_name="board_id",on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin,  related_name="pin_id",on_delete=models.CASCADE ,blank=True, null=True)



