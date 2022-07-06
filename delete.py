import boto3

ec2 = boto3.resource("ec2")


def delete_all_tail(name):
    _, *tail = ec2.images.filter(
        Filters=[{"Name": "name", "Values": [name]}], Owners=["self"]
    )

    def get_snapshot_id(image):
        [d["Ebs"]["SnapshotId"] for d in image.block_device_mappings if "Ebs" in d][0]

    for image in tail:
        image_name = image.name
        snapshot_id = get_snapshot_id(image)

        image.deregister()
        print(image_name + " deregistered")

        ec2.Snapshot(snapshot_id).delete()
        print(snapshot_id + " deleted")
