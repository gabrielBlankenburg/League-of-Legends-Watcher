from django.http import HttpResponse, JsonResponse


def generic_response(body={}, status_code=200):
	"""Returns the given status code and body as json.

	Parameters
	----------
	body : dict, optional
	status_code : int, optional

	Returns
	-------
	django.http.HttpResponse
	"""
	json_response = JsonResponse(body).content

	response = HttpResponse(status=200, content_type='application/json')
	response.write(json_response)
	return response