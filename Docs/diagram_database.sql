CREATE SCHEMA [ecommerce]
GO

CREATE TABLE [ecommerce].[merchants] (
  [id] int,
  [country_code] int,
  [merchant_name] nvarchar(255),
  [created at] nvarchar(255),
  [admin_id] int,
  PRIMARY KEY ([id], [country_code])
)
GO

CREATE TABLE [ecommerce].[order_items] (
  [order_id] int,
  [product_id] int,
  [quantity] int DEFAULT (1)
)
GO

CREATE TABLE [ecommerce].[orders] (
  [id] int PRIMARY KEY,
  [user_id] int UNIQUE NOT NULL,
  [status] nvarchar(255),
  [created_at] nvarchar(255)
)
GO

CREATE TABLE [ecommerce].[products] (
  [id] int PRIMARY KEY,
  [name] nvarchar(255),
  [merchant_id] int NOT NULL,
  [price] int,
  [status] nvarchar(255) NOT NULL CHECK ([status] IN ('out_of_stock', 'in_stock', 'running_low')),
  [created_at] datetime DEFAULT (now())
)
GO

CREATE TABLE [ecommerce].[product_tags] (
  [id] int PRIMARY KEY,
  [name] nvarchar(255)
)
GO

CREATE TABLE [ecommerce].[merchant_periods] (
  [id] int PRIMARY KEY,
  [merchant_id] int,
  [country_code] int,
  [start_date] datetime,
  [end_date] datetime
)
GO

CREATE TABLE [users] (
  [id] int PRIMARY KEY IDENTITY(1, 1),
  [full_name] nvarchar(255),
  [created_at] timestamp,
  [country_code] int
)
GO

CREATE TABLE [countries] (
  [code] int PRIMARY KEY,
  [name] nvarchar(255),
  [continent_name] nvarchar(255)
)
GO

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
  [ID] INT NOT NULL IDENTITY(1, 1),
  [channel_id] INT NOT NULL,
  [creator_id] INT NOT NULL,
  [created_at] DATETIME NOT NULL,
  [updated_at] DATETIME NOT NULL,
  [deleted_at] DATETIME NOT NULL,
  PRIMARY KEY ([ID], [channel_id])
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
  [email] text NOT NULL,
  [no_tlp] INT(12) NOT NULL,
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

CREATE TABLE [channel] (
  [ID] INT PRIMARY KEY NOT NULL,
  [channel_name] VARCHAR(50) NOT NULL,
  [created_at] DATETIME,
  [updated_at] DATETIME,
  [deleted_at] DATETIME
)
GO

CREATE INDEX [product_status] ON [ecommerce].[products] ("merchant_id", "status")
GO

CREATE UNIQUE INDEX [ecommerce].[products_index_1] ON [ecommerce].[products] ("id")
GO

CREATE UNIQUE INDEX [no_tlp_UNIQUE] ON [user] ("no_tlp")
GO

CREATE UNIQUE INDEX [email_UNIQUE] ON [user] ("email")
GO

CREATE UNIQUE INDEX [participants_UNIQUE] ON [participants] ("conversation_id", "user_id")
GO

CREATE UNIQUE INDEX [channel_name_UNIQUE] ON [channel] ("channel_name")
GO

EXEC sp_addextendedproperty
@name = N'Column_Description',
@value = 'When order created',
@level0type = N'Schema', @level0name = 'ecommerce',
@level1type = N'Table',  @level1name = 'orders',
@level2type = N'Column', @level2name = 'created_at';
GO

EXEC sp_addextendedproperty
@name = N'Column_Description',
@value = 'Sync the contacts to this table',
@level0type = N'Schema', @level0name = 'dbo',
@level1type = N'Table',  @level1name = 'contacts',
@level2type = N'Column', @level2name = 'ID';
GO

ALTER TABLE [ecommerce].[merchants] ADD FOREIGN KEY ([admin_id]) REFERENCES [users] ([id])
GO

ALTER TABLE [ecommerce].[merchants] ADD FOREIGN KEY ([country_code]) REFERENCES [countries] ([code])
GO

ALTER TABLE [ecommerce].[order_items] ADD FOREIGN KEY ([order_id]) REFERENCES [ecommerce].[orders] ([id])
GO

ALTER TABLE [ecommerce].[order_items] ADD FOREIGN KEY ([product_id]) REFERENCES [ecommerce].[products] ([id])
GO

ALTER TABLE [ecommerce].[products] ADD FOREIGN KEY ([merchant_id]) REFERENCES [ecommerce].[merchants] ([id])
GO

CREATE TABLE [ecommerce].[product_tags_products] (
  [product_tags_id] int,
  [products_id] int,
  PRIMARY KEY ([product_tags_id], [products_id])
);
GO

ALTER TABLE [ecommerce].[product_tags_products] ADD FOREIGN KEY ([product_tags_id]) REFERENCES [ecommerce].[product_tags] ([id]);
GO

ALTER TABLE [ecommerce].[product_tags_products] ADD FOREIGN KEY ([products_id]) REFERENCES [ecommerce].[products] ([id]);
GO


ALTER TABLE [ecommerce].[merchant_periods] ADD FOREIGN KEY ([merchant_id], [country_code]) REFERENCES [ecommerce].[merchants] ([id], [country_code])
GO

ALTER TABLE [users] ADD FOREIGN KEY ([country_code]) REFERENCES [countries] ([code])
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

ALTER TABLE [convo] ADD FOREIGN KEY ([channel_id]) REFERENCES [channel] ([ID])
GO
