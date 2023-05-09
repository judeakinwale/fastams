from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
import models
import schemas
import utils

router = APIRouter()


# [...] authenticate user
# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
@router.post('/', status_code=status.HTTP_201_CREATED)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
  login_details = payload.dict()
  email = login_details['email']
  password = login_details['password']
  user = utils.authenticate_user(email, password, db)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid email or password")
  token = utils.create_access_token(user)
  return {"status": "success", "data": user, "token": token}
# def login(email: str, password: str, db: Session = Depends(get_db)):
#   user = utils.authenticate_user(email, password, db)
#   if not user:
#     raise HTTPException(status_code=401, detail="Invalid email or password")
#   token = utils.create_access_token(user)
#   return {"status": "success", "data": user, "token": token}


# [...] get authenticated user
# @router.get('/me', response_model=schemas.User)
@router.get('/me')
def get_auth_user(current_user: models.User = Depends(utils.get_current_active_user)):
  user = current_user
  return {"status": "success", "data": user}

# // @desc    Forgot Password
# // @route   POST/api/v1/auth/forgotpassword
# // @access   Public
# exports.forgotPassword = asyncHandler(async (req, res, next) => {
#   const user = await User.findOne({ email: req.body.email });

#   if (!user) {
#     return next(new ErrorResponse("User not found", 404));
#   }
#   //Get reset token
#   const resetToken = user.getResetPasswordToken();
#   await user.save({ validateBeforeSave: false });

#   //Create reset url
#   const resetUrl = `${req.protocol}://${req.get(
#     "host"
#   )}/resetPassword/${resetToken}`;

#   const salutation = `Dear ${user.firstname ?? user.fullname}`;
#   const content = `You are receiving this email because you (or someone else) has requested
# the reset of a password, Please click on this button to complete your password reset \n\n <br /><br /> <a href="${resetUrl}" style="padding:1rem;color:black;background:#ff4e02;border-radius:5px;text-decoration:none;">Reset Password</a> \n\n <br /><br /> This link would expire in 10 minutes <br /><br/> Kindly ignore if you did not initate this request`;

#   try {
#     await sendEmail({
#       email: user.email,
#       subject: "Password reset token",
#       salutation,
#       content,
#     });
#     res.status(200).json({ success: true, data: user, message: "Email Sent" });
#   } catch (err) {
#     console.log(err);
#     user.getResetPasswordToken = undefined;
#     user.resetPasswordExpire = undefined;
#     // user.resetPasswordTokenExpire = undefined;

#     await user.save({ validateBeforeSave: false });
#     return next(new ErrorResponse("Email could not be sent", 500));
#   }

#   // res.status(200).json({
#   //   success: true,
#   //   data: user,
#   // });
# });
# [...] initiate forgot password
@router.post('/forgot-password')
def forgot_password(payload: schemas.ForgotPassword, db: Session = Depends(get_db)):
  update_data = payload.dict(exclude_unset=True)
  email = update_data['email']

  get_user = db.query(models.User).filter(models.User.email == email)
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this email: {email} found')

  update_data['reset_password_token'] = utils.generate_unique_token()

  get_user.filter(models.User.email == email).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(user)
  return {"status": "success", "data": user}
