Rails.application.routes.draw do
  get 'sessions/new'

  resources :users
  resources :sessions
  root to: 'users#splash'
  get '/auth/spotify/callback', to: 'users#new'
  get '/auth/spotify', as: 'spot_auth'

  get    '/selection',   to: 'users#unclassified_selection'
  get    '/class_playlists',   to: 'users#playlist_selection'

  get    '/login',   to: 'sessions#new'
  post   '/login',   to: 'sessions#create'
  delete '/logout',  to: 'sessions#destroy'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
