# cloudflare-dyndns
Update A Record via cloudflare api for dyndns functionality.


### Prerequisites
* Zone hosted at cloudflare
* Cloudflare API Token to edit desired zone
* Python3

### Install
`git clone https://github.com/MaEising/cloudflare-dyndns.git`
`export API_TOKEN=YOUR_CLOUDFLARE_TOKEN_HERE`
`python3 update_public_ip.py`

Use with cronjob or systemd timer to run daily.
Example systemd Unit and timer may be found under files.