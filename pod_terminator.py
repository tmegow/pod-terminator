import json
import logging
import os
import time

import argparse
import kubernetes

import timer_threads

SERVICE_TOKEN_FILENAME = os.getenv("SERVICE_TOKEN_FILENAME")
SERVICE_CERT_FILENAME = os.getenv("SERVICE_CERT_FILENAME")
KUBERNETES_HOST = "https://{}:{}".format(
    os.getenv("KUBERNETES_SERVICE_HOST"), os.getenv("KUBERNETES_SERVICE_PORT"))

def delete_pod(selector, namespace, api_instance):
    try:
        logging.info('Deleting pods with "{}" selector in {} namespace.'.format(
            selector, namespace))
        api_response = api_instance.delete_collection_namespaced_pod(
            namespace=namespace, pretty='true', label_selector=selector, timeout_seconds=120)
    except kubernetes.client.rest.ApiException as e:
        logging.error(
            "Exception when calling CoreV1Api->delete_collection_namespaced_pod: {}\n".format(e))


def main(args):
    # Configure logging
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    # Configure k8s client
    configuration = kubernetes.client.Configuration()
    configuration.host = KUBERNETES_HOST
    with open(SERVICE_TOKEN_FILENAME) as f:
        token = f.read()
        configuration.api_key['authorization'] = "bearer " + token.strip('\n')

    configuration.ssl_ca_cert = SERVICE_CERT_FILENAME
    kubernetes.client.Configuration.set_default(configuration)
    api_instance = kubernetes.client.CoreV1Api(
        kubernetes.client.ApiClient(configuration))

    # Read manifest and start timed threads
    with open(args.manifest) as f:
        manifest = json.load(f)

    for target in manifest["targets"]:
        selector_list = []
        for s in target["selector"]:
            selector_list.append(s + "=" + target["selector"][s])
        selector = ",".join(selector_list)
        timer_threads.RepeatedTimer(
            target["interval"], delete_pod, selector, target["namespace"], api_instance)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", help="absolute path to the YAML manifest file, where the list of pod roles is located",
                        default="/opt/manifest.json")
    args = parser.parse_args()
    main(args)
