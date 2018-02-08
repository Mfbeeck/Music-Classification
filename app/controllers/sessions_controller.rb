class SessionsController < ApplicationController
  def new
  end

  def create
	  user = User.find_by(id: params[:id])
	  if user && user.authenticate(params[:private_token])
	    session[:user_id] = user.id
	    redirect_to selection_path, notice: 'Logged in!'
	  else
	    redirect_to root_url
	  end
	end

	def destroy
    @id = current_user.id
	  session[:user_id] = nil
    user = User.find_by(id: @id)
    user.destroy
	  redirect_to root_url, notice: 'Done Here!'
	end
end
