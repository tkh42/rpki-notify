# myapp/models.py
from django.db import models


class Report(models.Model):
    time_stamp = models.DateTimeField()
    num_objects = models.IntegerField()
    num_roas = models.IntegerField()
    num_cas = models.IntegerField()
    num_overlap_vrps = models.IntegerField()
    num_diff_vrps = models.IntegerField()
    num_total_vrps = models.IntegerField()

    max_rp_exec_time = models.IntegerField()
    crawler_exec_time = models.IntegerField()


class RelyingParty(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="logs")
    name = models.CharField(max_length=100)
    num_vrps = models.IntegerField()


class ErrorMessage(models.Model):
    relying_party = models.ForeignKey(RelyingParty, on_delete=models.CASCADE, related_name="errors")
    message = models.TextField()
    count = models.IntegerField()


class Repository(models.Model):
    uri = models.URLField()
    reachable = models.BooleanField()
    num_affected_vrps = models.IntegerField()


class LogMessage(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="logs")
    relying_party = models.ForeignKey(RelyingParty, on_delete=models.CASCADE, related_name="availability_logs")
    log_entry = models.TextField()


class RelyingPartyLog(models.Model):
    relying_party = models.ForeignKey(RelyingParty, on_delete=models.CASCADE, related_name="logs") 
    log_entry = models.TextField()


class GhostbusterRecord(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="ghostbusters")
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Inconsistency(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="ghostbusters")
    file_name = models.CharField(max_length=100)
    log_message = models.TextField()


class Difference(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="ghostbusters")
    relying_party = models.CharField(max_length=100)
    vrp = models.CharField(max_length=1000)


class RegisteredUser(models.Model):
    name = models.TextField()
    email = models.TextField()

