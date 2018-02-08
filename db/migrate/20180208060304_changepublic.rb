class Changepublic < ActiveRecord::Migration[5.1]
  def change
    rename_column :playlists, :public, :public_bool
  end
end
