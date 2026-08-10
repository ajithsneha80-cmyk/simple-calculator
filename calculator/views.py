from django.shortcuts import render
from .models import Calculation
import requests
# Using sympify for safe math evaluation instead of eval()
from sympy import sympify

def calculator(request):
    if request.method == 'POST':
        expression = request.POST.get('expression')
        api_data = None

        # 1. Safe Evaluation
        try:
            # sympify converts string math safely without running arbitrary code
            result = str(sympify(expression).evalf())
        except Exception:
            result = "Error"

        # 2. Saving to Database
        Calculation.objects.create(
            expression=expression,
            result=result
        )

        # 3. Calling an External API inside the view (Example)
        if result != "Error":
            try:
                # Replace with your actual external URL, parameters, and headers
                api_url = "https://example.com"
                headers = {"Authorization": "Bearer YOUR_SECRET_KEY"}
                payload = {"expression": expression, "result": result}
                
                # Make the external call
                response = requests.post(api_url, json=payload, headers=headers, timeout=5)
                if response.status_code == 201:
                    api_data = response.json()
            except requests.RequestException:
                # Fail silently or log the error so your main user view doesn't crash
                api_data = {"status": "External API failed to log"}

        # 4. Rendering template with combined data
        return render(request, 'calculator/result.html', {
            'expression': expression,
            'result': result,
            'api_response': api_data
        })

    return render(request, 'calculator/index.html')
 
