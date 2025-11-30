"""
list all compute instances
"""
import oci
config=oci.config.from_file()
compute_client=oci.core.ComputeClient(config)
print("List of instances")
for meth in dir(compute_client) :
    if not meth.startswith("_"):
        print(meth)
list_instances=compute_client.list_instances(
    compartment_id="ocid1.tenancy.oc1..aaaaaaaa43chqgpy4hrunygnh5gb6upkoydhh4q6zna4xicrwdt7xigjbwya")
for instance in list_instances.data:
    print(instance.display_name)
# print(list_instances.data)
