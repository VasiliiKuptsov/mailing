# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user
    if user.groups.filter(name="managers").exists():
        context["is_in_group"] = self.request.user.groups.filter(
            name="managers"
        ).exists()
        context["all_mailings"] = (
            Mailing.objects.all().count()
            if Mailing.objects.all().count() > 0
            else 0
        )
        context["created_mailings"] = (
            Mailing.objects.filter(status=Mailing.CREATED).count()
            if Mailing.objects.filter().count() > 0
            else 0
        )
        context["active_mailings"] = (
            Mailing.objects.filter(status=Mailing.STARTED).count()
            if Mailing.objects.filter().count() > 0
            else 0
        )
        context["ended_mailings"] = (
            Mailing.objects.filter(status=Mailing.ENDED).count()
            if Mailing.objects.filter().count() > 0
            else 0
        )

    elif user.groups.filter(name="users").exists():
        context["all_mailings"] = (
            Mailing.objects.filter(owner=user).count()
            if Mailing.objects.filter(owner=user).count() > 0
            else 0
        )

        context["created_mailings"] = (
            Mailing.objects.filter(owner=user, status=Mailing.CREATED).count()
            if Mailing.objects.filter(owner=user).count() > 0
            else 0
        )
        context["active_mailings"] = (
            Mailing.objects.filter(owner=user, status=Mailing.STARTED).count()
            if Mailing.objects.filter(owner=user).count() > 0
            else 0
        )
        context["ended_mailings"] = (
            Mailing.objects.filter(owner=user, status=Mailing.ENDED).count()
            if Mailing.objects.filter(owner=user).count() > 0
            else 0
        )
    return context



self.fields["recipient"].queryset = Recipient.objects.filter(owner=user)


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user

    if user.groups.filter(name="users").exists():
        started_mailings = Mailing.objects.filter(
            status=Mailing.STARTED, owner=self.request.user
        )

        context["started_mailings"] = (
            AttemptMailing.objects.filter(
                mailing__in=started_mailings, owner=self.request.user
            ).count()
            if AttemptMailing.objects.filter(
                mailing__in=started_mailings, owner=self.request.user
            ).count()
               > 0
            else 0
        )

        context["count_attempts_mailings"] = (
            AttemptMailing.objects.filter(owner=self.request.user).count()
            if AttemptMailing.objects.filter(owner=self.request.user).count() > 0
            else 0
        )

        context["count_success_attempts_mailings"] = (
            AttemptMailing.objects.filter(
                status=AttemptMailing.SUCCESS, owner=self.request.user
            ).count()
            if AttemptMailing.objects.filter(
                status=AttemptMailing.SUCCESS, owner=self.request.user
            ).count()
               > 0
            else 0
        )

        context["count_not_success_attempts_mailings"] = (
            AttemptMailing.objects.filter(
                status=AttemptMailing.NOT_SUCCESS, owner=self.request.user
            ).count()
            if AttemptMailing.objects.filter(
                status=AttemptMailing.NOT_SUCCESS, owner=self.request.user
            ).count()
               > 0
            else 0
        )

    elif user.groups.filter(name="managers").exists():
        context["is_in_group"] = self.request.user.groups.filter(
            name="managers"
        ).exists()
        started_mailings = Mailing.objects.filter(status=Mailing.STARTED)

        context["started_mailings"] = (
            AttemptMailing.objects.filter(mailing__in=started_mailings).count()
            if AttemptMailing.objects.filter(mailing__in=started_mailings).count()
               > 0
            else 0
        )

        context["count_attempts_mailings"] = (
            AttemptMailing.objects.all().count()
            if AttemptMailing.objects.all().count() > 0
            else 0
        )

        context["count_success_attempts_mailings"] = (
            AttemptMailing.objects.filter(
                status=AttemptMailing.SUCCESS,
            ).count()
            if AttemptMailing.objects.filter(status=AttemptMailing.SUCCESS).count()
               > 0
            else 0
        )

        context["count_not_success_attempts_mailings"] = (
            AttemptMailing.objects.filter(status=AttemptMailing.NOT_SUCCESS).count()
            if AttemptMailing.objects.filter(
                status=AttemptMailing.NOT_SUCCESS
            ).count()
               > 0
            else 0
        )
    return context
