from django.core.validators import FileExtensionValidator
from django.db import models


class Animate(models.Model):
    #맨처음 이미지만 등록
    image = models.ImageField(upload_to='ani_image/', null=True, blank=True)
    #만화책 방향이 좌->우 인지 우->좌 인지 확인
    left_right_choice = (('좌', '좌->우'), ('우', '우->좌'))
    left_right = models.CharField(max_length=5, choices=left_right_choice, default='좌')
    # 웹툰형식인지 만화책형식인지 결정
    toon_comic_choice = (('T', '웹툰 형식'), ('C', '만화책형식'))
    toon_comic = models.CharField(max_length=5, choices=toon_comic_choice, default='T')
    # 영상 효과 결정
    ani_effect_choice = (('B', '말풍선'), ('N', '없음'))
    ani_effect = models.CharField(max_length=5, choices=ani_effect_choice, default='N')
    # 컷 전환효과 결정
    transition_effect_choice = (('D', '디졸브'), ('U', '위로 슬라이드'), ('Lt', '왼쪽으로 슬라이드'), ('Rt', '오른쪽으로 슬라이드'), ('N', '없음'))
    transition_effect = models.CharField(max_length=5, choices=transition_effect_choice, default='N')
    #분리되고 영상제작후 영상 파일 저장(mp4형식)
    ani = models.TextField(null=True, blank=True)
    #생성일자
    created_at = models.DateField(auto_now_add=True, null=True)


#다중이미지 처리를 위한 모델 생성
class AnimateImage(models.Model):
    animate = models.ForeignKey(Animate, on_delete=models.CASCADE, related_name='ani_id')
    image = models.ImageField(upload_to='ani_image/', null=True)
    image_base64 = models.TextField(null=True, blank=True)
    left_right = models.CharField(max_length=5, default='L')
    toon_comic = models.CharField(max_length=5, default='T')
    ani_effect = models.CharField(max_length=5, default='N')
    transition_effect = models.CharField(max_length=5, default='N')
