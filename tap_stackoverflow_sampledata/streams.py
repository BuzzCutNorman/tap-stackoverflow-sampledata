"""Stream type classes for tap-stackoverflow-sampledata."""
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_stackoverflow_sampledata.client import StackOverflowSampleDataStream


class BadgesStream(StackOverflowSampleDataStream):
    """Define custom stream."""
    name = "badges"
    file_name = "Badges.xml"
    primary_keys = ["Id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("Id", th.IntegerType),
        th.Property("UserId", th.StringType),
        th.Property("Name", th.StringType),
        th.Property("Date", th.DateTimeType),
        th.Property("Class", th.IntegerType),
        th.Property("TagBased", th.BooleanType),
    ).to_dict()


class CommentsStream(StackOverflowSampleDataStream):
    """Define custom stream."""
    name = "comments"
    file_name = "Comments.xml"
    primary_keys = ["Id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("Id", th.IntegerType),
        th.Property("PostId", th.IntegerType),
        th.Property("Score", th.IntegerType),
        th.Property("Text", th.StringType),
        th.Property("CreationDate", th.DateTimeType),
        th.Property("UserId", th.IntegerType),
        th.Property("ContentLicense", th.StringType),
    ).to_dict()


class PostLinksStream(StackOverflowSampleDataStream):
    """Define custom stream."""
    name = "postlinks"
    file_name = "PostLinks.xml"
    primary_keys = ["Id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("Id", th.IntegerType),
        th.Property("CreationDate", th.DateTimeType),
        th.Property("PostId", th.IntegerType),
        th.Property("RelatedPostId", th.IntegerType),
        th.Property("LinkTypeId", th.IntegerType),
    ).to_dict()


class PostsStream(StackOverflowSampleDataStream):
    """Define custom stream."""
    name = "posts"
    file_name = "Posts.xml"
    primary_keys = ["Id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("Id", th.IntegerType),
        th.Property("PostTypeId", th.IntegerType),
        th.Property("AcceptedAnswerId", th.IntegerType),
        th.Property("CreationDate", th.DateTimeType),
        th.Property("Score", th.IntegerType),
        th.Property("ViewCount", th.IntegerType),
        th.Property("Body", th.StringType),
        th.Property("OwnerUserId", th.IntegerType),
        th.Property("LastEditorUserId", th.IntegerType),
        th.Property("LastEditorDisplayName", th.StringType),
        th.Property("LastEditDate", th.DateTimeType),
        th.Property("LastActivityDate", th.DateTimeType),
        th.Property("Title", th.StringType),
        th.Property("Tags", th.StringType),
        th.Property("AnswerCount", th.IntegerType),
        th.Property("CommentCount", th.IntegerType),
        th.Property("FavoriteCount", th.IntegerType),
        th.Property("CommunityOwnedDate", th.DateTimeType),
        th.Property("ContentLicense", th.StringType),
    ).to_dict()


class TagsStream(StackOverflowSampleDataStream):
    """Define custom stream."""
    name = "tags"
    file_name = "Tags.xml"
    primary_keys = ["Id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("Id", th.IntegerType),
        th.Property("TagName", th.StringType),
        th.Property("Count", th.IntegerType),
        th.Property("ExcerptPostId", th.IntegerType),
        th.Property("WikiPostId", th.IntegerType),
    ).to_dict()


class UsersStream(StackOverflowSampleDataStream):
    """Define custom stream."""
    name = "users"
    file_name = "Users.xml"
    primary_keys = ["Id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("Id", th.IntegerType),
        th.Property("Reputation", th.IntegerType),
        th.Property("CreationDate", th.DateTimeType),
        th.Property("DisplayName", th.StringType),
        th.Property("LastAccessDate", th.DateTimeType),
        th.Property("AboutMe", th.StringType),
        th.Property("Views", th.IntegerType),
        th.Property("UpVotes", th.IntegerType),
        th.Property("DownVotes", th.IntegerType),
    ).to_dict()


class VotesStream(StackOverflowSampleDataStream):
    """Define custom stream."""
    name = "votes"
    file_name = "Votes.xml"
    primary_keys = ["Id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("Id", th.IntegerType),
        th.Property("PostId", th.IntegerType),
        th.Property("VoteTypeId", th.IntegerType),
        th.Property("CreationDate", th.DateTimeType),
    ).to_dict()
