# invitations/views.py
from django.urls import reverse
from .forms import InvitationForm
from google.oauth2 import service_account
import googleapiclient.discovery
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .models import Invitation


def save_to_google_sheets(invitation):
    credentials = service_account.Credentials.from_service_account_file(
        "django-database-405408-a49b35cd5b85.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )

    service = googleapiclient.discovery.build("sheets", "v4", credentials=credentials)

    spreadsheet_id = "1_VBC-iHHzu2Wne807oKn-21cKkCb_0Gg9aYAmEr0oWc"
    range_ = "Sheet1!A1"

    data = [
        [
            invitation.full_name,
            invitation.company,
            invitation.email,
            invitation.code,
            str(invitation.created_at),
        ]
    ]

    # Get the current data range in the sheet to determine where to append
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_)
        .execute()
    )
    num_rows = len(result.get("values", []))
    append_range = f"Sheet1!A{num_rows + 1}"

    # Append data to Google Sheets
    request = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=append_range,
            valueInputOption="RAW",
            body={"values": data},
        )
    )
    request.execute()


class CreateInvitationView(CreateView):
    model = Invitation
    form_class = InvitationForm
    template_name = "invitations/create_invitation.html"

    def form_valid(self, form):
        invitation = form.save(commit=False)

        # Generate and assign the incremented code
        new_code = (
            Invitation.increment_code()
        )  # Assuming increment_code() generates the code
        invitation.code = new_code

        # Save data to Google Sheets
        save_to_google_sheets(invitation)

        # Save the form data and redirect to the success URL with code
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("invitation_success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_choices"] = Invitation.COMPANY_CHOICES
        return context


class InvitationSuccess(TemplateView):
    template_name = "invitations/invitation_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_invitation = Invitation.objects.latest("id")  # Get the latest invitation
        context[
            "code"
        ] = latest_invitation.code  # Pass the code to the template context
        return context
