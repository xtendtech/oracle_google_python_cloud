import oci
import os
 
config = oci.config.from_file("C:\deve\py1\src\oracle/config")  # defaults to ~/.oci/config
compute_client = oci.core.ComputeClient(config)
print(compute_client)
compartment_id = "ocid1.tenancy.oc1..aaaaaaaa6jvzcanp5ntllp7extef2odlp2zctpillqrbnn2wki5eekxmghxa"
response = compute_client.list_instances(compartment_id='ocid1.tenancy.oc1..aaaaaaaa6jvzcanp5ntllp7extef2odlp2zctpillqrbnn2wki5eekxmghxa')
for instance in response.data:
    print(instance.display_name)
identity = oci.identity.IdentityClient(config)
# user = identity.get_user(config["user"]).data
# print(user)
database_client = oci.database.DatabaseClient(config)

# Send the request to service, some parameters are not required, see API
# doc for more info
list_db_system_shapes_response = database_client.list_db_system_shapes(
    compartment_id=compartment_id,
    availability_domain="us-ashburn-1")

# Get the data from response
# print(list_db_system_shapes_response.data)  
