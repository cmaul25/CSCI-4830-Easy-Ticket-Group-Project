from django.db import models
'''
Database structure of Easy Ticket: any new ticket is given each of 7 facts, such as a: Catagory(type of ticket), 
Priority level, status of ticket(open, closed, etc), comments attached, attachments, and who the ticket is from.
'''

#Type of ticket: Software Installation, Technical Issue, Slow computer
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

#Urgency. such as low, medium, high, emergency
class Priority(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField()

    #organizes tickets via their level
    class Meta:
        ordering = ['level']

    def __str__(self):
        return self.name

#Current state of the ticket, Open, In Progress, Pending, Closed
class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

#Main "model" of a submitted ticket, "all" information gathers here
class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    #User who generated the ticket
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets_created'
    )

    #User who is tasked with the ticket, notably, blank is possible if nobody has grabbed yet
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_assigned'
    )

    #tracking of previous classes for classification of the ticket
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)

    #Track updates and creation times
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Tracking for time sensitive tickets (can be empty for non-timed tickets)
    due_date = models.DateTimeField(null=True, blank=True)

    #Display ticket title
    def __str__(self):
        return self.title
        
    #Single database containing commonly searched information for faster queries
    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['created_at']),
        ]

#Comments made on a ticket, for tracking discussion and ticket updates
class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    #Author of the comment + comment itself
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    #When the comment was logged
    created_at = models.DateTimeField(auto_now_add=True)

#Attachments on ticket, such as screenshots, files, etc
class Attachment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    #Holds the file that was uploaded
    file = models.FileField(upload_to='ticket_attachments/')
    #Who uploaded it
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    #When the file was uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True)
