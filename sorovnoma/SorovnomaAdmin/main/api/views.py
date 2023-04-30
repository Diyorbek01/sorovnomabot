from rest_framework import viewsets
from django.db.models import Count, Sum, F
from rest_framework.decorators import permission_classes, api_view, action
from rest_framework.generics import get_object_or_404

from main.api.serializers import SorovnomaSerializer, RequiredChannelSerializer
from main.models import Sorovnoma, RequiredChannel, Variant, Vote
from rest_framework.response import Response
from datetime import timedelta, date, datetime
from main.models import User


class SorovnomaViewSet(viewsets.ModelViewSet):
    serializer_class = SorovnomaSerializer
    queryset = Sorovnoma.objects.filter(is_active=True).order_by('-created_at')

    @action(methods=['post'], detail=False)
    def create_sorovnoma(self, request):
        image = request.FILES.get('image')
        description = request.data.get('description')
        variants = request.data.get('variants')
        deadline = request.data.get('date')
        channels = request.data.get('channels')
        tg_id = request.data.get('user_id')
        today = date.today()
        real_date = today + timedelta(days=int(deadline))
        real_datetime = datetime.combine(real_date, datetime.min.time())
        user = User.objects.get(tg_id=tg_id)
        try:
            real_variants = variants.split(',')

            sorovnoma = Sorovnoma.objects.create(
                image=image,
                description=description,
                deadline=real_datetime,
                admin=user
            )
            for var in real_variants:
                var = var.replace(' ', "")
                instance = Variant.objects.create(name=var)
                sorovnoma.variants.add(instance)
                sorovnoma.save()
            if channels:
                channel_list = channels.split(',')
                for i in channel_list:
                    i = i.replace(' ', '')
                    required_channels = RequiredChannel.objects.create(
                        username=i,
                        sorovnoma=sorovnoma,
                        admin=user
                    )
            return Response({
                "id": sorovnoma.id,
                "image": sorovnoma.image.url,
                "description": sorovnoma.description,
                "deadline": sorovnoma.deadline,
                "variants": [i.name for i in sorovnoma.variants.all()],
                "status": 201
            })

        except Exception as e:
            return Response(
                {
                    "msg": "Fail",
                    "status": 400
                }
            )

    @action(methods=['get'], detail=False)
    def get_sorovnoma(self, request):
        tg_id = request.GET.get('tg_id')
        sorovnomalar = Sorovnoma.objects.filter(is_active=True, admin__tg_id=tg_id)
        serializers = SorovnomaSerializer(sorovnomalar, many=True)
        return Response(serializers.data)

    @action(methods=['get'], detail=False)
    def cancel_sorovnoma(self, request):
        id = request.GET.get('id')
        sorovnoma = Sorovnoma.objects.get(id=id)
        sorovnoma.is_active = False
        sorovnoma.save()
        return Response({"msg": "Success"})

    @action(methods=['get'], detail=False)
    def get_details(self, request):
        id = request.GET.get('id')
        sorovnoma = get_object_or_404(Sorovnoma, id=id)
        serializers = SorovnomaSerializer(sorovnoma)
        return Response(serializers.data)

    @action(methods=['get'], detail=False)
    def voting(self, request):
        variant_id = request.GET.get('variant')
        tg_id = request.GET.get('tg_id')
        sorovnoma = Sorovnoma.objects.filter(variants__in=[variant_id])
        user = get_object_or_404(User, tg_id=tg_id)
        if sorovnoma.exists():
            if not Vote.objects.filter(user=user, sorovnoma=sorovnoma.last()).exists():
                vote = Vote.objects.create(
                    variant_id=variant_id,
                    sorovnoma=sorovnoma.last(),
                    user=user
                )
                return Response({"msg": "Success", "variant": vote.variant.name}, status=201)
        return Response({"msg": "Error"}, status=400)

    @action(methods=['post'], detail=False)
    def create_admin(self, request):
        full_name = request.data.get('full_name')
        tg_id = request.data.get('tg_id')
        phone_number = request.data.get('phone_number', None)
        user = request.data.get('user', None)
        if user is None:
            try:
                if not User.objects.filter(tg_id=tg_id).exists():
                    User.objects.create(full_name=full_name, tg_id=tg_id, phone_number=phone_number, is_admin=True)
                    return Response({"msg": "success"}, status=201)
                else:
                    user = User.objects.get(tg_id=tg_id)
                    user.full_name = full_name
                    user.phone_number = phone_number
                    user.is_admin = True
                    user.save()
                    return Response({"msg": "success"}, status=201)
            except Exception as e:
                return Response({"msg": "Something went wrong"}, status=400)
        else:
            try:
                if not User.objects.filter(tg_id=tg_id).exists():
                    User.objects.create(full_name=full_name, tg_id=tg_id)
                    return Response({"msg": "Success", "status": 201})
                else:
                    user = User.objects.get(tg_id=tg_id)
                    return Response({"msg": "User exists", "role": user.is_admin, "status": 402})
            except Exception as e:
                return Response({"msg": "Something went wrong"}, status=400)

    @action(methods=['get'], detail=False)
    def verify_human(self, request):
        tg_id = request.GET.get('tg_id')
        user = get_object_or_404(User, tg_id=tg_id)
        user.is_human = True
        user.save()
        return Response({"msg": "Success"}, status=200)

    @action(methods=['get'], detail=False)
    def check_human(self, request):
        tg_id = request.GET.get('tg_id')
        user = get_object_or_404(User, tg_id=tg_id)

        return Response({"msg": user.is_human}, status=200)

    @action(methods=['post'], detail=False)
    def update_deadline(self, request):
        id = request.data.get('id')
        days = request.data.get('day')
        sorovnoma = get_object_or_404(Sorovnoma, id=id)
        real_date = sorovnoma.deadline + timedelta(days=int(days))
        real_datetime = datetime.combine(real_date, datetime.min.time())
        sorovnoma.deadline = real_datetime
        sorovnoma.save()
        return Response({"msg": "Success"}, status=200)


class RequiredChannelViewSet(viewsets.ModelViewSet):
    serializer_class = RequiredChannelSerializer
    queryset = RequiredChannel.objects.all()

    @action(methods=['get'], detail=False)
    def get_channels(self, request):
        tg_id = request.GET.get('tg_id')
        channels = RequiredChannel.objects.filter(admin__tg_id=tg_id, is_active=True).values('username').annotate(
            joined_users=Sum('number_of_joined_users'),
            planed_users=Sum('number_of_planed_users'),
            id=Count('id')
        ).order_by('username')
        return Response(channels)

    @action(methods=['get'], detail=False)
    def get_channels_variant(self, request):
        varinat_id = request.GET.get('variant')
        sorovnomas = Sorovnoma.objects.filter(variants__in=[varinat_id])
        channels = []
        for i in RequiredChannel.objects.filter(sorovnoma=sorovnomas.last(), is_active=True):
            channels.append({"name": i.username})
        return Response(channels)

    @action(methods=['post'], detail=False)
    def set_plan_channels(self, request):
        tg_id = request.data.get('tg_id')
        channel_id = request.data.get('channel_id')
        number = request.data.get('number')

        channels = RequiredChannel.objects.filter(username=channel_id, is_active=True)
        for i in channels:
            i.number_of_planed_users = number
            i.save()
        return Response({"msg": "Success"}, status=200)

    @action(methods=['get'], detail=False)
    def joined_user(self, request):
        sorovnoma_id = request.GET.get('id')

        sorovnoma = get_object_or_404(Sorovnoma, id=sorovnoma_id)
        channels = RequiredChannel.objects.filter(sorovnoma=13, is_active=True)
        for i in channels:
            i.number_of_joined_users += 1
            i.save()
        return Response({"msg": "Success"}, status=200)

    @action(methods=['get'], detail=False)
    def get_all_users(self, request):

        users = [i.tg_id for i in User.objects.all()]
        return Response(users)
