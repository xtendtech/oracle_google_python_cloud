import oci
import os

print(os.getcwd())

config = oci.config.from_file( )  # defaults to ~/.oci/config
compute_client = oci.core.ComputeClient(config)


# previously retrieved information for so that we don't have to make redundant service
# calls
subnet_info = {}
vcn_info = {}

# This dictionary stores which public IP address a private IP (identified via its OCID)
# is assigned to
private_ip_to_public_ip = {}
instance_id = "ocid1.instance.oc1.phx.anyhqljtd4a42rqczs56mmahs6rvqufqinlfgbgfn2pnlu45herqy3ry35va"

compart_id = config["tenancy"]
identity_client = oci.identity.IdentityClient(config)
compute_client = oci.core.ComputeClient(config)

response = identity_client.list_region_subscriptions(compart_id)

# resp= compute_client.list_images(compart_id)
# print(resp.data)

# config = oci.config.from_file("config")
compute_client = oci.core.ComputeClient(
    config, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY
)
virtual_network_client = oci.core.VirtualNetworkClient(
    config, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY
)
identity_client = oci.identity.IdentityClient(
    config, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY
)
blstorage = oci.core.BlockstorageClient(
    config, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY
)
 