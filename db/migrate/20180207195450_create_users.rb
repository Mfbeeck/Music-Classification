class CreateUsers < ActiveRecord::Migration[5.1]
  def change
    create_table :users do |t|
      t.string :spotify_id
      t.string :spotify_name
      t.string :private_token
      t.string :refresh_token
      t.string :model
      t.string :fit


      t.timestamps
    end
  end
end
