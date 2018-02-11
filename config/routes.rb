Rails.application.routes.draw do
  get 'sessions/new'

  resources :users
  resources :sessions
  resources :tracks, only: :index

  root to: 'users#splash'
  get '/auth/spotify/callback', to: 'users#get_playlists'
  get '/auth/spotify', as: 'spot_auth'
  post 'get_tracks',   to: 'users#get_tracks'
  get '/get_playlists',   to: 'users#get_playlists'

  get    '/selection',   to: 'users#unclassified_selection'
  get    '/class_playlists',   to: 'users#choose_playlists'
  get    '/choose',  to: 'users#choose_tracks'
  get    '/classified',  to: 'users#classified'
  get    '/classification',  to: 'users#classification'
  get    '/complete',  to: 'users#complete'
  post    '/pushing_tracks',  to: 'users#pushing_tracks'

  get    '/login',   to: 'sessions#new'
  post   '/login',   to: 'sessions#create'
  delete '/logout',  to: 'sessions#destroy'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
