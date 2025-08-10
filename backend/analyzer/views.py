# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
# import PyPDF2

# class DocumentAnalysisView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request):
#         file = request.FILES.get('document')
#         if not file:
#             return Response({'error': 'No file uploaded'}, status=400)

#         pdf_reader = PyPDF2.PdfReader(file)
#         text = ''
#         for page in pdf_reader.pages:
#             text += page.extract_text() or ''

#         # Basic keyword presence check (customize as needed)
#         required_keywords = [
#             "HS Code", "Goods Description", "Unit of measure", "Quantity",
#             "Weight", "Value", "Currency", "Shipper", "Consignee",
#             "Container Number", "Port of discharge"
#         ]

#         missing = [kw for kw in required_keywords if kw.lower() not in text.lower()]
#         result = "All required fields found." if not missing else f"Missing fields: {', '.join(missing)}"

#         return Response({'result': result})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import PyPDF2

class DocumentAnalysisView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            file = request.FILES.get('document')
            if not file:
                return Response({'result': 'No file uploaded'}, status=400)

            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            if not text.strip():
                return Response({'result': 'No readable text found in the PDF (might be scanned image).'}, status=400)

            required_keywords = [
                "HS Code", "Goods Description", "Unit of measure", "Quantity",
                "Weight", "Value", "Currency", "Shipper", "Consignee",
                "Container Number", "Port of discharge", "BOL", "AWB"
            ]

            missing = [kw for kw in required_keywords if kw.lower() not in text.lower()]
            result = "All required fields found." if not missing else f"Missing fields: {', '.join(missing)}"

            return Response({'result': result})

        except Exception as e:
            return Response({'result': f'Error analyzing document: {str(e)}'}, status=500)
