CREATE TABLE [user] (
  [ID] INT PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [no_tlp] VARCHAR(12) NOT NULL,
  [email] VARCHAR(100) NOT NULL,
  [password] VARCHAR(40) NOT NULL,
  [first_name] VARCHAR(20) NOT NULL DEFAULT '',
  [last_name] VARCHAR(20) NOT NULL DEFAULT '',
  [created_at] DATETIME NOT NULL,
  [updated_at] DATETIME NOT NULL,
  [photo_profile] BLOB
)
GO

CREATE TABLE [user_verification] (
  [user_id] INT NOT NULL,
  [verification_code] VARCHAR(45) NOT NULL,
  [created_at] VARCHAR(45) NOT NULL
)
GO

CREATE TABLE [message] (
  [ID] INT PRIMARY KEY NOT NULL,
  [guid] VARCHAR(100) NOT NULL,
  [convo_id] INT NOT NULL,
  [sender_id] INT NOT NULL,
  [message_type] nvarchar(255) NOT NULL CHECK ([message_type] IN ('text', 'image', 'video', 'audio')) NOT NULL,
  [message] VARCHAR NOT NULL DEFAULT '',
  [created_at] DATETIME NOT NULL,
  [deleted_at] DATETIME NOT NULL
)
GO

CREATE TABLE [convo] (
  [ID] INT PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [creator_id] INT NOT NULL,
  [created_at] DATETIME NOT NULL,
  [updated_at] DATETIME NOT NULL,
  [deleted_at] DATETIME NOT NULL
)
GO

CREATE TABLE [participants] (
  [ID] INT PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [conversation_id] INT NOT NULL,
  [user_id] INT NOT NULL,
  [type] nvarchar(255) NOT NULL CHECK ([type] IN ('single', 'group')) NOT NULL,
  [created_at] DATETIME NOT NULL,
  [updated_at] DATETIME NOT NULL
)
GO

CREATE TABLE [user_contact] (
  [user_id] INT NOT NULL,
  [contact_id] INT NOT NULL,
  [first_name] VARCHAR(20) NOT NULL DEFAULT '',
  [last_name] VARCHAR(20) NOT NULL DEFAULT '',
  [created_at] DATETIME NOT NULL,
  [updated_at] DATETIME NOT NULL,
  PRIMARY KEY ([user_id], [contact_id])
)
GO

CREATE TABLE [contacts] (
  [ID] INT PRIMARY KEY NOT NULL,
  [first_name] VARCHAR(20) NOT NULL DEFAULT '',
  [last_name] VARCHAR(20) NOT NULL DEFAULT '',
  [email] VARCHAR(100) NOT NULL,
  [no_tlp] VARCHAR(12) NOT NULL,
  [created_at] VARCHAR(45) NOT NULL
)
GO

CREATE TABLE [attachments] (
  [ID] INT PRIMARY KEY NOT NULL,
  [message_id] INT NOT NULL,
  [file_url] VARCHAR(50) NOT NULL,
  [created_at] TIMESTAMP NOT NULL,
  [updated_at] DATETIME
)
GO

CREATE UNIQUE INDEX [no_tlp_UNIQUE] ON [user] ("no_tlp")
GO

CREATE UNIQUE INDEX [email_UNIQUE] ON [user] ("email")
GO

CREATE UNIQUE INDEX [participants_UNIQUE] ON [participants] ("conversation_id", "user_id")
GO

EXEC sp_addextendedproperty
@name = N'Column_Description',
@value = 'Sync the contacts to this table',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'contacts',
@level2type = N'Column', @level2name = 'ID';
GO

ALTER TABLE [user_verification] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([ID])
GO

ALTER TABLE [message] ADD FOREIGN KEY ([sender_id]) REFERENCES [user] ([ID])
GO

ALTER TABLE [convo] ADD FOREIGN KEY ([creator_id]) REFERENCES [user] ([ID])
GO

ALTER TABLE [message] ADD FOREIGN KEY ([convo_id]) REFERENCES [convo] ([ID])
GO

ALTER TABLE [participants] ADD FOREIGN KEY ([conversation_id]) REFERENCES [convo] ([ID])
GO

ALTER TABLE [participants] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([ID])
GO

ALTER TABLE [user_contact] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([ID])
GO

ALTER TABLE [user_contact] ADD FOREIGN KEY ([contact_id]) REFERENCES [contacts] ([ID])
GO

ALTER TABLE [attachments] ADD FOREIGN KEY ([message_id]) REFERENCES [message] ([ID])
GO
