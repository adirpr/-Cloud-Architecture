import io
import json
import logging
import oci

from fdk import response


def handler(ctx, data: io.BytesIO=None):
    if None == ctx.RequestURL():
        return "Function loaded properly but not invoked via an HTTP request."
    signer = oci.auth.signers.get_resource_principals_signer()
    logging.getLogger().info("URI: " + ctx.RequestURL() )
    config = {
        "tenancy": "ocid1.tenancy.oc1..aaaaaaaa224ppyilguxb5kdap23totog3qgmafsuwj7gemo66nsskqdcaafq",
        "region": "il-jerusalem-1"
    }
    try:
        object_storage = oci.object_storage.ObjectStorageClient(config, signer=signer)
        namespace = object_storage.get_namespace().data
        bucket_name = "exercise_1"
        file_object_name = ctx.RequestURL()
        if file_object_name.endswith("/"):
            logging.getLogger().info("Adding index.html to reques URL " + file_object_name)
            file_object_name += "index2.html"

        # strip off the first character of the URI (i.e. the /)
        file_object_name = file_object_name[1:]

        obj = object_storage.get_object(namespace, bucket_name, file_object_name)
        return response.Response(
            ctx, response_data=obj.data.content,
            headers={"Content-Type": obj.headers['Content-type']}
        )
    except (Exception) as e:
        return response.Response(
            ctx, response_data=e,
            headers={"Content-Type": "text/plain"}
            )