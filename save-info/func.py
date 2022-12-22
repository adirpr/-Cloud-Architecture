import io
import json
import logging
import oci

from fdk import response


def handler(ctx, data: io.BytesIO=None):
    if None == ctx.RequestURL():
        return "Function loaded properly but not invoked via an HTTP request."
    logging.getLogger().info(ctx.Method())
    if ctx.Method() != "POST":
        return "Function loaded properly but not invoked as post method"
    signer = oci.auth.signers.get_resource_principals_signer()
    logging.getLogger().info("URI: " + ctx.RequestURL() )
    config = {
        "tenancy": "ocid1.tenancy.oc1..aaaaaaaa224ppyilguxb5kdap23totog3qgmafsuwj7gemo66nsskqdcaafq",
        "region": "il-jerusalem-1"
    }
    try:
        file_n = "info.txt"
        object_storage = oci.object_storage.ObjectStorageClient(config, signer=signer)
        namespace = object_storage.get_namespace().data
        bucket_name = "exercise_1"

        body = json.loads(data.getvalue())
        info = body.get("info")
        get_object_response = object_storage.get_object(namespace, bucket_name, file_n)
        console.log(get_object_response)
        content = get_object_response.data.content.decode() + '\n' + info
        console.log(content)
        obj1 = object_storage.put_object(namespace, bucket_name, file_n, content)

    except (Exception, ValueError) as ex:
        logging.getLogger().info('error: ' + str(ex))
		
    return response.Response(
        ctx, response_data=content + "bamba!!!" obj1,
        headers={"Content-Type": "application/json"}
    )