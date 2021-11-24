import datetime
import requests
import base64
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from rest_framework.renderers import JSONRenderer

from animateapp.forms import AnimateForm
from animateapp.models import Animate, AnimateImage

#json을 만들어 보내기전에 가지고 있는 이미지 파일을
#충돌 오류 때문에 기록...
import os

from animateapp.serializers import PreprocessedImageSerializer

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


class AnimateCreateView(CreateView):
    model = Animate
    form_class = AnimateForm
    template_name = 'animateapp/create.html'

    def post(self, request, *args, **kwargs):
        #form받아옴 -
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #이미지 파일들만 받아오기
        files = request.FILES.getlist('image')
        #Animate 모델에는 첫이미지만 저장되게 하기
        form.instance.image = files[0]
        animate = form.save(commit=False)
        animate.save()

        if form.is_valid():
            #이미지 파일 np array형식으로 저장하기위한 리스트 생성
            # 선택값들 받아오기
            l_r = str(form.instance.left_right)
            t_c = str(form.instance.toon_comic)
            ani_effect = str(form.instance.ani_effect)
            tran_effect = str(form.instance.transition_effect)

            #이미지 파일을 하나씩 불러와서 np array형식으로 image_list에 저장
            for f in files:
                animate_image = AnimateImage(animate=animate, image=f, image_base64="", left_right=l_r, toon_comic=t_c,
                                             ani_effect=ani_effect, transition_effect=tran_effect)
                animate_image.save()
                path = 'media/' + str(animate_image.image)
                animate_image.image_base64 = base_64_encode(path)
                animate_image.save()

            id = animate.id
            objects = AnimateImage.objects.filter(animate=id)
            post_json = PreprocessedImageSerializer(objects, many=True)#데이터베이스에 있는 파이썬 객체를 dictionary로 변환해줍니다.
            renderer = JSONRenderer()
            json_data = renderer.render(post_json.data) #직렬화를 통한 dictionary를 json으로 바꿔줍니다.
            headers = {'Content-Type': 'application/json'}
            url = "http://127.0.0.1:8000/models/model/" #post를 보낼 url을 지정
            res = requests.post(url, data=json_data, headers=headers) #json형태로 data를 보냅니다.respone으로 url을 받아 옵니다
            # model_server로 부터 받은 데이터를 처리
            respone_url = 'http://127.0.0.1:8000/media/' + str(res.text)[1:-1]
            animate = form.save(commit=False)
            animate.ani = respone_url
            animate.save()

            return HttpResponseRedirect(reverse('animateapp:detail', kwargs={'pk': animate.pk}))
        else:
            return self.form_invalid(animate)


class AnimateDetailView(DetailView):
    model = Animate
    context_object_name = 'target_animate'
    template_name = 'animateapp/detail.html'

#array형태를 base64형태로 바꾸는 함수
def base_64_encode(path):
    with open(path, 'rb') as img:
        base64_string = base64.b64encode(img.read())
        tmp = str(base64_string)[2:-1]
        return tmp
