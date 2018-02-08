require 'rspotify/oauth'

Rails.application.config.middleware.use OmniAuth::Builder do
  provider :spotify, ENV['spotify_client_id'], ENV['spotify_client_secret'], callback: nil, scope: 'user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-library-read user-library-modify'
end
