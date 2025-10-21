from django.shortcuts import render

# Create your views here.
# strings/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import django_filters
from .analyzer import analyze_string


class StringFilter(django_filters.FilterSet):
    # Filters corresponding to: ?is_palindrome=true
    is_palindrome = django_filters.BooleanFilter(field_name='is_palindrome')
    
    # Filters corresponding to: ?min_length=5
    min_length = django_filters.NumberFilter(field_name='length', lookup_expr='gte')
    
    # Filters corresponding to: ?max_length=20
    max_length = django_filters.NumberFilter(field_name='length', lookup_expr='lte')
    
    # Filters corresponding to: ?word_count=2
    word_count = django_filters.NumberFilter(field_name='word_count')
    
    # Filters corresponding to: ?contains_character=a (case-insensitive check on the 'value' field)
    contains_character = django_filters.CharFilter(field_name='value', lookup_expr='icontains')

    class Meta:
        model = AnalyzedString
        # Include any fields you want to filter directly without a custom definition (e.g., ?length=10)
        fields = ['is_palindrome', 'length', 'word_count'] 

class StringListCreateAPIView(generics.ListCreateAPIView):
    """Handles both GET (List/Filter) and POST (Creation/Analysis) on /strings/."""
    queryset = AnalyzedString.objects.all()
    serializer_class = AnalyzedStringSerializer
    
    # Filtering settings (inherited from StringListView)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = StringFilter 
    ordering_fields = ['length', 'word_count', 'created_at'] 

    def create(self, request, *args, **kwargs):
        """Overrides the POST method to include custom analysis and error handling."""
        value = request.data.get('value')
        
        # --- (Place your full custom POST logic here, exactly as it was in the post() method of StringListCreateView) ---
        
        # 1. Error Handling: 400/422 Checks for 'value' existence and type
        if value is None:
            return Response({"error": "Missing 'value' field in request body."}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(value, str):
            return Response({"error": "'value' must be a string."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # 2. Analysis and 409 Conflict Check
        analysis_data = analyze_string(value)
        if AnalyzedString.objects.filter(pk=analysis_data['id']).exists():
            return Response({"error": "String already exists in the system."}, status=status.HTTP_409_CONFLICT)
        
        # 3. Create/Save Instance
        instance = AnalyzedString.objects.create(
            # Pass all fields from analysis_data to create the instance
            id=analysis_data['id'], value=analysis_data['value'],
            length=analysis_data['length'], is_palindrome=analysis_data['is_palindrome'],
            unique_characters=analysis_data['unique_characters'], word_count=analysis_data['word_count'],
            character_frequency_map=analysis_data['character_frequency_map']
        )
        
        # 4. Success Response
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# --- 1C. GET /strings/{sha256_hash} (Detail View) ---
class StringDetailView(generics.RetrieveAPIView):
    """Handles GET /api/strings/{hash} for retrieving a single string."""
    queryset = AnalyzedString.objects.all()
    serializer_class = AnalyzedStringSerializer
    # This tells DRF to use the URL variable (pk) to look up the primary key (id, which is the hash)
    lookup_field = 'pk' 
    # If the hash is not found, DRF automatically returns a 404 Not Found response.

class StringRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = AnalyzedString.objects.all()
    serializer_class= AnalyzedStringSerializer
    lookup_field = 'pk'

class NaturalLanguageView(APIView):
    def get(self,request):
        query_text = request.query_params.get('query', '')

        if not query_text:
            return Response(
                {"error": "Missing 'query' "},
                status= status.HTTP_400_BAD_REQUEST
            )
        
        interpreted_filters={}
        
        if "single word palindromic strings" in query_text.lower():
            # Example: "all single word palindromic strings"
            interpreted_filters['is_palindrome'] = 'true'
            interpreted_filters['word_count'] = 1
        
        elif "longer than 10 characters" in query_text.lower():
            # Example: "strings longer than 10 characters"
            interpreted_filters['min_length'] = 11
            
        elif "contain the letter z" in query_text.lower():
            # Example: "strings containing the letter z"
            interpreted_filters['contains_character'] = 'z'
        
        elif not interpreted_filters:
            # Handle unparsable/unsupported queries
            return Response(
                {"error": "Unable to parse natural language query."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- STEP 2: Apply Filters and Get Results ---
        # Create a temporary queryset based on the interpreted filters
        queryset = StringListView.queryset.all()
        filterset = StringFilter(interpreted_filters, queryset=queryset)
        
        if not filterset.is_valid():
             # 422 Unprocessable Entity: Query parsed but resulted in conflicting/invalid filters
             return Response(
                {"error": "Interpreted query resulted in invalid filter parameters."}, 
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        filtered_data = filterset.qs
        
        # --- STEP 3: Format Success Response ---
        serializer = StringListView.serializer_class(filtered_data, many=True)
        
        return Response({
            "data": serializer.data,
            "count": filtered_data.count(),
            "interpreted_query": {
                "original": query_text,
                "filters_applied": interpreted_filters
            }
        }, status=status.HTTP_200_OK)
    


