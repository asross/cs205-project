set :haml, { :ugly => true, :format => :html5 }
set :css_dir, 'stylesheets'
set :js_dir, 'javascripts'
set :images_dir, 'images'

sprockets.append_path File.join root, 'bower_components'
sprockets.import_asset 'bootstrap/fonts/glyphicons-halflings-regular.woff' do |p|
  "#{fonts_dir}/glyphicons-halflings-regular.woff"
end
sprockets.import_asset 'bootstrap/fonts/glyphicons-halflings-regular.woff2' do |p|
  "#{fonts_dir}/glyphicons-halflings-regular.woff2"
end

configure :build do
  activate :relative_assets
end

helpers do
  def references
    {
      'wormhole' => 'Lan, Shiwei, Jeffrey Streets, and Babak Shahbaba. "Wormhole Hamiltonian Monte Carlo." Proceedings of the AAAI Conference on Artificial Intelligence. AAAI Conference on Artificial Intelligence. Vol. 2014. NIH Public Access, 2014.',
      'topicmodes' => 'Roberts, Margaret, Brandon Stewart, and Dustin Tingley. "Navigating the local modes of big data: The case of topic models." 2015.'
    }
  end

  def render_references
    return "<ol>#{references.map{|k,v| "<li id='ref-#{k}'>#{v}</li>"}.join("\n")}</ol>".html_safe
  end

  def cite(ref)
    return "[<a href='#ref-#{ref}'>#{references.keys.index(ref)+1}</a>]".html_safe
  end
end

Dotenv.load

if ENV.key?('S3_BUCKET')
  activate :s3_sync do |s3_sync|
    s3_sync.bucket                     = ENV['S3_BUCKET']
    s3_sync.region                     = ENV['S3_REGION']
    s3_sync.aws_access_key_id          = ENV['AWS_ACCESS_KEY_ID']
    s3_sync.aws_secret_access_key      = ENV['AWS_SECRET_ACCESS_KEY']
    s3_sync.delete                     = false # We delete stray files by default.
    s3_sync.after_build                = false # We do not chain after the build step by default.
    s3_sync.prefer_gzip                = true
    s3_sync.path_style                 = true
    s3_sync.reduced_redundancy_storage = false
    s3_sync.acl                        = 'public-read'
    s3_sync.encryption                 = false
    s3_sync.version_bucket             = false
  end
end
