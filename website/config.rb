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
      'climate' => 'Solonen, Antti, et al. "Efficient MCMC for climate model parameter estimation: parallel adaptive chains and early rejection." Bayesian Analysis 7.3 (2012): 715-736.',
      'forecast' => 'Geweke, John, and Charles Whiteman. "Bayesian forecasting." Handbook of economic forecasting 1 (2006): 3-80.',
      'physics' => 'Ceperley, D. M. "Metropolis methods for quantum Monte Carlo simulations." AIP Conference Proceedings. Ed. James E. Gubernatis. Vol. 690. No. 1. AIP, 2003.',
      'wormhole' => 'Lan, Shiwei, Jeffrey Streets, and Babak Shahbaba. "Wormhole Hamiltonian Monte Carlo." Proceedings of the AAAI Conference on Artificial Intelligence. AAAI Conference on Artificial Intelligence. Vol. 2014. NIH Public Access, 2014.',
      'darting' => 'Ahn, Sungjin, Yutian Chen, and Max Welling. "Distributed and Adaptive Darting Monte Carlo through Regenerations." AISTATS. 2013.',
      'topicmodes' => 'Roberts, Margaret, Brandon Stewart, and Dustin Tingley. "Navigating the local modes of big data: The case of topic models." 2015.',
      'secondeig' => 'Haveliwala, Taher, and Sepandar Kamvar. The second eigenvalue of the Google matrix. Stanford, 2003.',
      'convspeed' => 'Backåker, Fredrik. The Google Markov Chain: convergence speed and eigenvalues. Diss. Master Thesis, Uppsala University, Sweden, 2012.',
      'pagerank' => 'Page, Lawrence, et al. The PageRank citation ranking: Bringing order to the web. Stanford InfoLab, 1999.',
      'tempering' => 'Radford M. Neal (1996). "Sampling from multimodal distributions using tempered transitions". Statistics and Computing. 6 (4): 353–366.',
      'restarts' => 'Barrett, Leon, and Aleksandr Simma. "MCMC With Disconnected State Spaces." (2005).',
      'hmc' => 'Neal, Radford M. "MCMC using Hamiltonian dynamics." Handbook of Markov Chain Monte Carlo 2 (2011): 113-162.'
    }
  end

  def render_references
    return "<ol>#{references.map{|k,v| "<li id='ref-#{k}'>#{v}</li>"}.join("\n")}</ol>".html_safe
  end

  def cite(ref)
    return "[<a href='#ref-#{ref}'>#{references.keys.index(ref)+1}</a>]".html_safe
  end

  def check
    return "<input type='checkbox' checked disabled/>"
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
