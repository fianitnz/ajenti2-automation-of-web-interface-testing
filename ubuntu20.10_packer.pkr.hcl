# source "qemu" "ubuntu server to manage with ajenti" {
source "qemu" "ubuntu" {

# Image
    #iso_url           = "https://releases.ubuntu.com/20.04.1/ubuntu-20.04.1-live-server-amd64.iso"
    iso_url           = "../distributive/ubuntu-20.04.1-live-server-amd64.iso"
    iso_checksum      = "sha256:443511f6bf12402c12503733059269a2e10dec602916c0a75263e5d990f6bb93"
    iso_target_path   = "../distributive/"
    #output_directory = "./ajenti"

# Disk
    format      = "qcow2"
    disk_size   = "3000M"

# System
    vm_name     = "ajenti_test"

    accelerator     = "kvm"
    cpus            = "2"
    memory          = "2048"
    disk_interface  = "virtio"
    net_device      = "virtio-net"
    headless        = "false"

    #http_directory         = "path/to/httpdir"

    boot_wait               = "3s"
    boot_key_interval       = "0.1s"
    boot_keygroup_interval  = "2s"
    boot_command            = [
            "<enter><enter><enter>",
            "<wait1m40s>",

        # Configuration
            #lang   updat  key          netw   prox   mirr
            "<enter><enter><enter><wait><enter><enter><enter>",

        # Disk
            #smal s avail dev          add gpt par              create
            "<enter><enter><down><down><enter><down><down><down><enter>",
            #                        done         cont d
            "<down><down><down><down><enter><down><enter>",

        # Profile setup
            #name                 server name        user name
            "<insert>qwerty<down><insert>qwerty<down><insert>qwerty<down>",
            #password            confirm
            "<insert>qwerty<down><insert>qwerty<down><enter>",

        # SSH Setup
            "<spacebar><down><down><enter>",

        # Featured Server Snaps
            #pass
            "<tab><enter>",

        # Wait instalation system
            "<wait20m>",

        # Instalation complete
            "<enter><wait10s><enter>",
            #"<rightCtrlOn><rightAltOn><f2><rightCtrlOff><rightAltOff>"
    ]

    communicator            = "ssh"
    pause_before_connecting = "20m"
    ssh_username            = "qwerty"
    ssh_password            = "qwerty"
    ssh_timeout             = "20m"

    #shutdown_timeout        = "10m"
    #shutdown_command        = "echo 'packer' | sudo -S shutdown -P now"

}

build {
  sources = ["source.qemu.ubuntu"]
}
