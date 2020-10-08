from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2048)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.CharField(max_length=2048, blank=True)
    category = models.CharField(max_length=64, blank=True)
    watchlist_user = models.ManyToManyField(
        User, blank=True, related_name='watchlist_item')
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} by {self.owner} bidding starts at {self.starting_bid}$ : {self.description}'

    def current_bid(self):
        try:
            a = self.bids.all()[0]
            return f"{a.bid}$"
        except:
            return f"No current Bids"

    def winner(self):
        try:
            a = self.bids.all()[0]
            return f"{a.bid_by} won the auction by bidding {a.bid}$"
        except:
            return f"No one won this listing"


class Comments(models.Model):
    commented_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commented")
    commented_on = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.commented_by} commented on {self.commented_on.title}: {self.comment}"


class Bids(models.Model):
    bid_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bids_made_by_user')
    bid_on = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name='bids')
    bid = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.bid_by} placed {self.bid} on {self.bid_on.title}"
