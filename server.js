require('dotenv').config()

const express = require('express')
const req = require('express/lib/request')
const app =  express()
const mongoose = require('mongoose')

mongoose.connect(process.env.DATABSE_URL)
const db = mongoose.connection
db.on('error', (error) => console.error(error))
db.on('open', () => console.log('Connected to Database'))


app.listen(3000, () => console.log('Server Started'))