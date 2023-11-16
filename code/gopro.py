import os
import shutil
import urllib.request
import re
import json
import sys
import requests
import time

from MediaElement import MediaElement


class GoProManager:
	def __init__(self, email, password, path):
		if sys.version_info[0] < 3:
			print("Python 3 is needed.")
			exit()
		# Constants:
		self.GOPRO_API_ENDPOINT = "https://api.gopro.com"
		self.GOPRO_API_OAUTH2_TOKEN = "https://api.gopro.com/v1/oauth2/token"
		self.GOPRO_API_GET_MEDIA = "https://api.gopro.com/media/search"
		self.GOPRO_API_CLIENT_ID = "71611e67ea968cfacf45e2b6936c81156fcf5dbe553a2bf2d342da1562d05f46"
		self.GOPRO_API_CLIENT_SECRET = "3863c9b438c07b82f39ab3eeeef9c24fefa50c6856253e3f1d37e0e3b1ead68d"
		self.path = path
		self.USER_EMAIL = email
		self.USER_PASSWORD = password
		self.pages = None
		self.pageCounter = 1

	def getToken(self):
		data = {
			"client_id": self.GOPRO_API_CLIENT_ID,
			"client_secret": self.GOPRO_API_CLIENT_SECRET,
			"grant_type": "password",
			"scope": "root root:channels public me upload media_library_beta live",
			"username": self.USER_EMAIL,
			"password": self.USER_PASSWORD
		}
		data_encoded = urllib.parse.urlencode(data).encode("utf-8")
		response = urllib.request.urlopen(self.GOPRO_API_OAUTH2_TOKEN, data_encoded).read()
		jsonResponse = json.loads(response)
		return jsonResponse["access_token"]

	def getMediaList(self):
		headers = {
			'Accept-Charset': 'utf-8',
			'Accept': 'application/vnd.gopro.jk.media+json; version=2.0.0',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + self.getToken()
		}

		mediaMetaDataList = []

		thumbnailURL = "https://images-02.gopro.com/resize/450wwp/"
		for index in range(1,self.pages):

			url = self.GOPRO_API_GET_MEDIA + "?fields=captured_at,content_title,content_type,created_at,gopro_user_id,file_size,id,token,type,resolution,filename,file_extension&per_page=50&page=" + str(index)
			request = urllib.request.Request(url, headers=headers)
			resp = urllib.request.urlopen(request)
			content = resp.read()

			#remove b and ' at the beginning of the file to create json format
			content = str(content)
			content = content[1:]
			content = content[1:]
			content = content[:-1]
			print(content)
			json_content = json.loads(content)
			x = 1
			for elem in json_content["_embedded"]["media"]:

				#thumbnailRequest = urllib.request.Request((thumbnailURL + str(elem["token"])), headers=headers)
				#thumbnailResponse = urllib.request.urlopen(thumbnailRequest)
				if not elem["id"] == "3ay9wVXzM79Ww":
					print("elem: " + str(elem["id"]) + " - " + str(elem["filename"]))
					print((thumbnailURL + str(elem["token"])))
					thumbnail = requests.get((thumbnailURL + str(elem["token"])), stream=True).content
					if elem["filename"] == '':
						f = open(x, 'wb')
					else:
						f = open(elem["filename"], 'wb')

					# Storing the image data inside the data variable to the file
					f.write(thumbnail)
					f.close()



		#mediaMetaDataList.append(
					#MediaElement(id=elem["id"], filename=elem["filename"], date=elem["captured_at"], fileSize=elem["file_size"],
								# fileExtension=elem["file_extension"],
								 #thumbnail=thumbnailResponse))

		print("Media: " + str(len(mediaMetaDataList)))
		return mediaMetaDataList




	def downloadMedia(self, id, type, path):
		token = self.getToken()
		params = {'fields': 'id,filename,file_extension'}
		headers = {
			'Accept-Charset': 'utf-8',
			'Accept': 'application/vnd.gopro.jk.media+json; version=2.0.0',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer %s' % token
		}
		url = self.GOPRO_API_ENDPOINT + "/media/" + id + "/download"
		response = requests.get(url, params=params, headers=headers)
		response.raise_for_status()

		content = response.json()
#TODO: check if file is video or not
		if type == "Video":
			filename = content["filename"]
			fileURL = content["_embedded"]["variations"][2]["url"]
			videoPath = os.path.join(path, "videos")

			print("START DOWNLOADING Video: " + filename + "\n")
			video = requests.get(fileURL, stream=True)

			total_length = video.headers["Content-Length"]
			with open(os.path.join(videoPath,filename), 'wb') as f:
				if total_length is None:  # no content length header
					f.write(video.content)
				else:
					dl = 0
					total_length = int(total_length)
					for data in video.iter_content(chunk_size=4096):
						dl += len(data)
						f.write(data)
						done = int(50 * dl / total_length)
						sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
						sys.stdout.flush()


	def checkConnection(self):
		url = "%s/media/search" % self.GOPRO_API_ENDPOINT
		token = self.getToken()
		params = {'fields': 'id,filename,file_extension'}
		headers = {
			'Accept-Charset': 'utf-8',
			'Accept': 'application/vnd.gopro.jk.media+json; version=2.0.0',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer %s' % token
		}
		response = requests.get(url, params=params, headers=headers)
		response.raise_for_status()
		self.pages = response.json()["_pages"]["total_pages"]
		print("Pages: " + str(self.pages))
		return response.status_code


	def downloadVideo(self):
		url = "https://media-cdn-us-west-2.gopro.com/ef21d0b6-03f3-4a74-9261-8016edc4761c/2493982906410600088/source/default/1.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA3OOFXGVANNB537O7%2F20231027%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20231027T221904Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEG4aCXVzLXdlc3QtMiJIMEYCIQD5BLFQFtblwqVeBKAk2A8W%2BvEBVkpGICxRgidwyaxDNwIhAMD9YS01V%2Frgp5lUbMM6z3xgJ2W%2Bf0OvqCuWNANX0575KoUFCJf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNzg2OTMwNTQ1OTg0IgydIAX2DczRfk4LU5oq2QSucNw3eKMa72wNkbX%2FJDgbLiKnrxU6BmwV3jFUC5g3eliwd106kmmPK42fweZy8pBYiG36w%2BhT%2BPZPy0SS8FdFokdJX%2FqtY9ZppyMaS9spPP76%2Fj8CC%2FXFO5PdkedAFiiqlN5EaoOcH9MB%2BCuVEe8F8DwFdTQ9kXH9Ehss69%2F%2Bg5YF4xr3amo1y2WBl%2BuKUR4u%2BjbDooJFT8pNfz12uQ9DcHAuhL2A8PixhCcoonJFFcYPbbcZLYkyjm0CqG%2B4SAtq1qxWQo6pAITE2y6rtolCCWDY3GyQdMX%2BBbCOLtXBNaKESxkdvQdYRVCe19evl5yuuqomg%2BmTgp20naMCKyGfBdrzQCI4UIFlhOj4hn6s6TqAmmzrJUNHEmSwPraF1Y1pMphUOWB5%2BnWrBahJbdzIUfhNMKsW93WVrG4QiCFZuu5JzYtdpDOd52KnIDFMbdMH0mBSpG%2F2jDYn2lhmnEu5sigg4w53S%2Bk2AAWRP7xcpwwzOYxi%2BlBJlLAfUMNzePjd%2BCdVd5QO4bAYVIOAfhx7ytwe2WIobQBNscEvagu4rXPv5d%2B%2FLLR533dVWBaSTYnI0TtQm4Eu48Gdg2HCQwKQyYs78UBRRsM86ajoJD0yCDwo7up8QUXzFTmEWhtnWLunKKT5gXz6zqpOAfPa7aW7%2F%2FVsMJKsKwg3c8%2FcjQSQmZAlpQHnhWYP%2Bng9Bc5hJeS0HCQRwSK95XxvtrKDXnJm2kJaMkfZRsiUxGlqPDAjEGfv9kmn6I4yEto7zl4cxjtUYsJYEaYQ2o5f%2BvTFfsW5gUuzyamxVVpaMJLt8KkGOpkBF8stIUD2S7TN0YBQ%2BGoX3t6V4iiholZprXT8Hu32yAldoHg3cgR7HE11cuajDAO7t6pshh7uQrR0TGauCCg%2FpuChQVBIAYPhBFWq0uxVT97WL1NmMHaYup6ZW9v7pbMv8sPb5Nz5JzLd%2FjedAgCBL1OgSvzC006Wj%2BBk%2FhMVFkwYraBPycMCAnoCTuFV8iQFp4MFGqgSaEaQ&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DGH010279.MP4%3B&X-Amz-Signature=1b3cb61c9154b5785e5722817a24a932c1af3b2b473c436b6d4894fa004ed735"
		urllib.request.urlretrieve(url, "goproplus/testfile.mp4")
		print("done")