import airbyte
from airbyte.models import shared, operations
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from customers.models import ConnectionKey

airbyte_api = airbyte.Airbyte(
    security=shared.Security(
        bearer_auth=settings.AIRBYTE_API_ACCESS_TOKEN,
    ),
)


def generate_oauth_link_from_key(request, connection_key: str):
    connection_key = get_object_or_404(ConnectionKey, pk=connection_key)

    request = shared.InitiateOauthRequest(
        o_auth_input_configuration=shared.OAuthInputConfiguration(),
        redirect_url=f"{settings.HOSTNAME}/{reverse('oauth_redirect_with_secret', args=[connection_key.connection_key])}",
        source_type=shared.OAuthActorNames.SHOPIFY,
        workspace_id=connection_key.connection.customer.workspace_id,
    )

    response = airbyte_api.sources.initiate_o_auth(request)
    if response.status_code != 200:
        # TODO: Handle this error
        return None

    return redirect(response.redirect_url)


def oauth_redirect_with_secret(request, connection_key: str):
    secret_id = request.GET.get("secret_id")
    connection_key = get_object_or_404(ConnectionKey, connection_key=connection_key)

    request = operations.PatchSourceRequest(
        source_patch_request=shared.SourcePatchRequest(
            secret_id=secret_id
        ),
        source_id=connection_key.connection.source_id
    )

    response = airbyte_api.sources.patch_source(request)

    if response.status_code != 200:
        # TODO: Figure out what happened.
        return None

    # TODO: Show a message to the user that things are good
    return None
