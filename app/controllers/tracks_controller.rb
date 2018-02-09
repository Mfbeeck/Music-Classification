class TracksController < ApplicationController
  def index
    @Tracks = current_user.all

    respond_to do |format|
      format.html
      format.csv { send_data @Tracks.to_csv, filename: "mytracks.csv" }
    end
  end
end
