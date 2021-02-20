from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transactions
from .serializers import TransactionSerializer
from rest_framework.views import APIView

# Create your views here.
@api_view(['GET'])
def get_all_points(request):
    queryset = Transactions.objects.all()
    result_serializer = TransactionSerializer(queryset, many=True)
    result = {}
    for element in result_serializer.data:
        if element["payer"] in result:
            result[element["payer"]] += element["points"]
        else:
            result[element["payer"]] = element["points"]
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_transaction(request):
    post_data = request.data
    print(post_data)
    transaction_data = TransactionSerializer(data=post_data)
    if transaction_data.is_valid():
        transaction_data.save()
        return Response({"Details":"Success"}, status=status.HTTP_200_OK)
    else:
        print(transaction_data.errors)
        return Response({"Error":"Bad details"}, status=status.HTTP_400_BAD_REQUEST)
    

class spend_points(APIView):
    def __init__(self):        
        self.queryset = Transactions.objects.all().order_by('timestamp')
        self.result_serializer = TransactionSerializer(self.queryset, many=True)
        self.sorted_result = self.result_serializer.data
        self.update_points = 0
        self.result = []

    def update_record(self, points, id):
        update_record = Transactions.objects.get(pk=id)
        update_record.points = points
        update_record.save()

    def create_result(self, item, append):
        temp = {}
        new_points = 0
        old_points = 0
        if not any(temp_iter['payer'] == item['payer'] for temp_iter in self.result):                
            temp['payer'] = item['payer']
            if not append:
                temp['points'] = self.points
                self.update_points = item['points'] - self.points
            else:
                temp['points'] = item['points']
            self.result.append(temp)           
            self.update_record(self.update_points, item['id'])
        else:
            old_points = [x['points'] for x in self.result if x['payer'] == item['payer']]
            if not append:
                self.update_points = item['points'] - self.points
                new_points = self.points + old_points[0]
            else:
                new_points = item['points'] + old_points[0]
            for name in self.result:                    
                if name['payer'] == item['payer']:
                    name['points'] = new_points            
            self.update_record(self.update_points, item['id'])

    def post(self, request):
        self.points = request.data["points"]
        for item in self.sorted_result:
            if self.points > 0:
                if self.points > item['points']:
                    self.points -=item['points']
                    self.create_result(item, True)
                else:
                    self.create_result(item, False)                    
                    self.points = 0

        for i in self.result:
            i['points'] = -i['points']                

        return Response(self.result, status=status.HTTP_200_OK)