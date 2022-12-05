CREATE TABLE [channel] (
  [id] INT PRIMARY KEY NOT NULL,
  [owner_id] INT,
  [member_id] int,
  [name] VARCHAR(50) NOT NULL,
  [description] VARCHAR(50),
  [created_at] DATETIME,
  [updated_at] DATETIME
)
GO

CREATE TABLE [user] (
  [user_id] INT,
  [channel_id] INT
)
GO

ALTER TABLE [channel] ADD FOREIGN KEY ([owner_id]) REFERENCES [user] ([user_id])
GO

ALTER TABLE [channel] ADD FOREIGN KEY ([id]) REFERENCES [user] ([channel_id])
GO

ALTER TABLE [user] ADD FOREIGN KEY ([channel_id]) REFERENCES [channel] ([member_id])
GO
