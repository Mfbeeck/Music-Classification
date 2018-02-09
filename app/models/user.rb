class User < ApplicationRecord
  validates_presence_of :classif_type
  validates_presence_of :private_token
  has_many :playlists, dependent: :destroy
  has_many :tracks, dependent: :destroy


end
