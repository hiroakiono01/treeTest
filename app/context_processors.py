from app.models import Client, CurrentClient


def global_data(self):
    try:
        # currentClient = CurrentClient.objects.all().first()
        currentClient = CurrentClient.objects.filter(customUser=self.user).all().first()
        client = Client.objects.filter(id=currentClient.client_id).first()
        client_name = client.client_name
        client_no = client.client_no
        client_id = client.pk
    except:
        client_name = '対象の事業者がありません。'
        client_no = ''
        client_id = ''

    return {'client_name': client_name,
            'client_no': client_no,
            'client_id': client_id,
            }
