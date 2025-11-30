from pathlib import Path
import oci
# import logging
from oci.config import validate_config

# logging.getLogger('oci').setLevel(logging.DEBUG)
# config['log_requests'] = True
# logging.basicConfig()

# Configuration 
config = oci.config.from_file("C:/Users/cochi/.oci/config") 
""" sample_config= {
    'log_requests' : 'True',
    'additional_user_agent' :'',
    'pass_phrase' :'None',
    'user' :'ocid1.user.oc1..aaaaaaaa3q3m2pw42oqjhuftykoorhqjim7ktlqnuym6',
    'fingerprint' :'48:b1:e4:aa:a2:29:06:77:aa:a5:45:16:cb: ',
    'tenancy' :'ocid1.tenancy.oc1..aaaaaaaa43chqgpy4hrunygnh5gb6upkoydhh4q6zna4x',
    'region' :'ap-mumbai-1',   
    'key_file' :'C:\\Users\\cochi\\.oci\\key.pem',
     }
"""
validate_config(config)
client = oci.identity.IdentityClient(config)
# This call will emit log information to stderr
print(client.list_regions())
# # Instance details
INSTANCE_NAME = "oraind3"
COMPARTMENT_ID =config["tenancy"]
SUBNET_ID = "ocid1.subnet.oc1.ap-mumbai-1.aaaaaaaahwkqbiutejg2ngb6fugscpiyvg5yr57wbrdzy37kpvlraws5renq"  # Your subnet OCID
IMAGE_ID = "ocid1.image.oc1.ap-mumbai-1.aaaaaaaarkpc5y2ufls3xeb4o6jh2wbmzzleklbkjkfvhxqcvwof5yf2l5gq"  # Ubuntu Mumbai
OPERATING_SYSTEM = 'Canonical Ubuntu'

SSH_PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCfmtfdunI/jbvolinpESOZdm3GEsz8ePs+yo6tX+AEhkVpTGw8AGuT5saghcuyF0TwPIxMpH8gtKTZvdcXbdzdL33dX201Pj/aCG4A2IFcQv5Ucg/F7JS52oq69+oPcrMCNELGYjyDvYK2t4KaOe69t3MmdpYC8MBmxTanGmuuP1UGc6BViH5Kn48L1QXqsE75MBHWXLMemD36P9y7l0atQ4JVkmKM9TAJFLIzeiRl1NB70coHHoojfR1oLljjB2QbLuEILybFnitFkVqn1WuW3Oz2JMR03vPoNqKbuvgjRA8KS4g72aX6ku/76E14tUCrM1IfxhexLa+LBiAs13rEG/vo7mxE3zcgNP7oAROC1viV2oY4pDFUspF+FN8kNNkiBOO0lu33Jpx4ZIg/gVAgbbqoofLubCfnCFPMo+hwVlva9+9v1ZB3PmWMqiCm38Pl0KukFvXBEdbI8r143dD8DJryCT5mxbkCDyRXjKwscWCPJ8UF0euozFoui8RNhLOAlPrJbrUR6gJJN1b9wq7Kikdqe+vIiw6cn6AOXFTB8Rda4MgzWYoNNGEMDoM2xltoOnYuPKqLdf/BirWugZI0whpWDtncmAz5X0dPoY4lXlprKsG35PsHwBstzsQpTSuX+2FF2Pe519jfU95YimqBHqg/g+CnGiPuj9mGUsKRQQ== root@99978" 
SSH_PUBLIC_KEY_PATH= Path(config["key_file"] )
# print(SSH_PUBLIC_KEY_PATH)
def read_ssh_public_key(file_path:Path)->str:
    if file_path.is_file:
     with open(file_path,"r") as pub_key:
        SSH_PUBLIC_KEY=pub_key.read()
    else:
     print("Public Key File not found")
    return ( SSH_PUBLIC_KEY)
        
# SSH_PUBLIC_KEY=read_ssh_public_key(SSH_PUBLIC_KEY_PATH)
 
SHAPE="VM.Standard.A1.Flex"
OCPUS = 2  # Free tier allows up to 4 OCPUs total
MEMORY_IN_GBS = 12  # Free tier allows up to 24GB total
# Request wait time (seconds)
REQUEST_WAIT_TIME_SECS = 60

# Initialize compute client
compute_client = oci.core.ComputeClient(config)
identity_client = oci.identity.IdentityClient(config)

def get_availability_domain(identity_client, compartment_id):
    list_availability_domains_response = oci.pagination.list_call_get_all_results(
        identity_client.list_availability_domains,
        compartment_id
    )
    # For demonstration, we just return the first availability domain but for Production code you should
    # have a better way of determining what is needed
    availability_domain = list_availability_domains_response.data[0] 
    # print('Running in Availability Domain: {}'.format(availability_domain.name))
    return availability_domain.name

AVAILABILITY_DOMAIN = get_availability_domain(identity_client, COMPARTMENT_ID)

def get_shape(compute_client,COMPARTMENT_ID, AVAILABILITY_DOMAIN):
    """
    This function is used to get availble shapes in the Availbility
    """
    list_shapes_response = oci.pagination.list_call_get_all_results(
        compute_client.list_shapes,
        compartment_id=COMPARTMENT_ID,
        availability_domain=AVAILABILITY_DOMAIN
    )
    shapes = list_shapes_response.data
    if len(shapes) == 0:
        raise RuntimeError('No available shape was found.')

    vm_shapes = list(filter(lambda shape: shape.shape.startswith("VM"), shapes))
    if len(vm_shapes) == 0:
        raise RuntimeError('No available VM shape was found.')

    # For demonstration, we just return the first shape but for Production code you should have a better
    # way of determining what is needed
    shape = vm_shapes[0]

    # print('Found Shape: {}'.format(shape.shape))

    return shape

 
shape= get_shape(compute_client, COMPARTMENT_ID, AVAILABILITY_DOMAIN)
def get_image(compute, compartment_id, shape):
    # Listing images is a paginated call, so we can use the oci.pagination module to get all results
    # without having to manually handle page tokens
    #
    # In this case, we want to find the image for the operating system we want to run, and which can
    # be used for the shape of instance we want to launch
    list_images_response = oci.pagination.list_call_get_all_results(
        compute.list_images,
        compartment_id,
        operating_system=OPERATING_SYSTEM,
        shape=shape.shape
    )
    images = list_images_response.data
    if len(images) == 0:
        raise RuntimeError('No available image was found.')

    # For demonstration, we just return the first image but for Production code you should have a better
    # way of determining what is needed
    image = images[0]

    # print('Found Image: {}'.format(image.id))
    # print()

    return image
# print( get_image(compute_client, COMPARTMENT_ID, shape))
 
 
def launch_instance():
    """Launch VM.Standard.A1.Flex instance"""
    
    instance_details = oci.core.models.LaunchInstanceDetails(
        availability_domain=AVAILABILITY_DOMAIN,
        compartment_id=COMPARTMENT_ID,
        shape= SHAPE,
        display_name=INSTANCE_NAME,

        # Shape config for flexible shapes
        shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
            ocpus=OCPUS, memory_in_gbs=MEMORY_IN_GBS
        ),

        # Source details (image)
        source_details=oci.core.models.InstanceSourceViaImageDetails(
            source_type="image",
            image_id=IMAGE_ID,
            boot_volume_size_in_gbs=50,  # Minimum boot volume size
        ),
        
        # Network details
        create_vnic_details=oci.core.models.CreateVnicDetails(
            subnet_id=SUBNET_ID, assign_public_ip=False

        ),
        # SSH key
        metadata={"ssh_authorized_keys": SSH_PUBLIC_KEY},
    )
 
     
    try:
        response = compute_client.launch_instance(instance_details)
        instance = response.data
        print("Instance launched successfully!")
        print(f"Instance ID: {instance.id}")
        print(f"Instance Name: {instance.display_name}")
        print(f"State: {instance.lifecycle_state}")
        return instance
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error: {e.message}")
        if e.status == 500 and "Out of host capacity" in str(e):
            print(
                f"✗ Out of capacity error. Retrying in {REQUEST_WAIT_TIME_SECS} seconds..."
            )
            return None
        else:
            print(f"✗ Error: {e.message}")
            raise


def main():
    """Main function with retry logic"""
    # print(f"Attempting to create {INSTANCE_NAME} (VM.Standard.A1.Flex)...")
    # print(f"Configuration: {OCPUS} OCPUs, {MEMORY_IN_GBS}GB RAM")

    attempt = 0
    while True:
        attempt += 1
        print( "main")
        launch_instance()
        exit(0)
# main()
launch_instance()