import Router from 'express'
import multer from 'multer'
import { auth } from '../middleware/auth'
// 加载环境变量
import dotenv from 'dotenv'
dotenv.config()

export const router = Router()

// 配置multer的存储选项
const storage = multer.diskStorage({
  destination(req, file, cb) {
    cb(null, process.env.UPLOAD_FOLDER) // 确保这个文件夹存在
  },
  filename(req, file, cb) {
    cb(null, `${file.fieldname}-${Date.now()}.${file.originalname.split('.').pop()}`)
  },
})

const upload = multer({ storage })
router.post('/upload-image', auth, upload.single('file'), async (req, res) => {
  try {
    if (!req.file)
      res.send({ status: 'Fail', message: '没有文件被上传', data: null })
    const data = {
      fileKey: req.file.filename,
    }
    // 文件已上传
    res.send({ status: 'Success', message: '文件上传成功', data })
  }
  catch (error) {
    res.send(error)
  }
})
