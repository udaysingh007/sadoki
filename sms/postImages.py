import cloudinary
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from constants import const as cn

cloudinary.config( 
  cloud_name = cn.CLOUDINARY_NAME, 
  api_key = cn.CLOUDINARY_API_KEY, 
  api_secret = cn.CLOUDINARY_API_SECRET 
)

def uploadFile(filename, tag=cn.CLOUDINARY_TAG):
    response = upload(filename, tags=tag)
    url, options = cloudinary_url(
        response['public_id'],
        format=response['format']
    )
    return url
    
def cleanup(tag=cn.CLOUDINARY_TAG):
    response = resources_by_tag(tag)
    resources = response.get('resources', [])
    if not resources:
        # print("No images found")
        return
    # print("Deleting {0:d} images...".format(len(resources)))
    delete_resources_by_tag(tag)
    # print("Done!")


print ("Tag: ", cn.CLOUDINARY_TAG)

cleanup()

uploadFile("/home/pi/sadoki/snapshot.jpg")
