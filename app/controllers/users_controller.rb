class UsersController < ApplicationController
  def splash

  end

  # def spotify
  #   spotify_user = RSpotify::User.new(request.env['omniauth.auth'])
  #   # Now you can access user's private data, create playlists and much more
  #   redirect_to root_url(email: spotify_user)
  # end

  def new
    # if request.env['omniauth.auth'].nil?
    #   redirect_to root_url, notice: 'You must sign into Spotify first'
    # end
    # @spotify_user = RSpotify::User.new(request.env['omniauth.auth'])
    @user = User.new()
    @@oauth = request.env['omniauth.auth']
  end

  def create
    @user = User.new(user_params)

    if !@@oauth.nil?
      @spot_json = @@oauth.credentials
      @spot_user_info = @@oauth.info
      @user.private_token = @spot_json['token']
      @user.refresh_token = @spot_json['refresh_token']
      @user.spotify_name = @spot_user_info.display_name
      @user.spotify_id = @spot_user_info.id
    end
    # require 'net/http'
    # scopes = 'user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-library-read user-library-modify'
    # redirect_url = 'http://localhost:3000'
    # url_base = "https://accounts.spotify.com/authorize/?client_id=" + ENV['spotify_client_id'] + "&response_type=code&redirect_uri=" + redirect_url + "&scope=" + scopes + "&state=34fFs29kd09"
    # url = URI.parse(url_base)
    # redirect_to url
    # tokens = `python /Users/matiasbeeck/Documents/metis/metisgh/project3/autoclassify/lib/assets/python_scripts/get_tokens.py #{ENV['spotify_client_id']} #{ENV['spotify_client_secret']}`
    # @user.access_token = spotify_user['token']
    # @user.private_token = tokens[1]

    if @user.save
      user = User.find_by(id: @user.id)
      if user
  	    session[:user_id] = user.id
        if current_user.classif_type == 'library'
          redirect_to class_playlists_path, notice: 'Logged in!'
        else
          require 'json'
          # playlists = JSON.parse(`python /Users/matiasbeeck/Documents/metis/metisgh/project3/autoclassify/lib/assets/python_scripts/get_my_playlists.py #{current_user.private_token}`)
          playlists = JSON.parse(`python /Users/matiasbeeck/Documents/metis/metisgh/project3/autoclassify/lib/assets/python_scripts/get_my_playlists.py 'BQCzxXtxazQKdb79LJEKvhxxYy2At0KyiSMve_QaCSBRyhTr1_llc-KQFtvtBVQo1ZplrDvxnrsB1lj0KlhOM62wymg7BWI05jbK10VVIMhcG692VWE501jbjScl73D_Amqm20ILkqXZoOSx8NvsKVmJQ5RRC1ke1xwM2gvsk66ucQay-BFOi9jC_dTP8s2PLoHl-Mksg2jTahevSsqw_vJPyjJW1zx5ToPOo2w'`)
          for playlist in playlists
            @play = Playlist.new()
            @play.playlist_name = playlist[0]
            @play.track_count = playlist[1]
            @play.owner = playlist[2]
            @play.owner_id = playlist[3]
            @play.playlist_url = playlist[4]
            @play.playlist_id = playlist[5]
            @play.playlist_artwork = playlist[6]
            @play.collaborative = playlist[7]
            @play.public_bool = playlist[8]
            @play.user_id = current_user.id
            @play.save
          end

          redirect_to selection_path, notice: 'Logged in!'
        end
    else
      redirect_to root_url, notice: 'Nope!'
    end
    else
      redirect_to root_url, notice: 'You must sign into Spotify first'
    end
  end

  def playlist_selection
  end

  def unclassified_selection
    @playlists = current_user.playlists
  end


  private

  def user_params
    params.require(:user).permit(:oauth, :classif_type, :spotify_id, :spotify_name, :private_token, :refresh_token, :model, :fit)
  end
end
