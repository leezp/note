-- TeamViewer wireshark decoder
-- still pretty incomplete
-- @drspringfield

tv_proto = Proto ("teamviewer","TeamViewer")

local f_magic = ProtoField.uint16("teamviewer.magic", "Magic", base.HEX)

tv_commands = {}
tv_commands[10] = "CMD_IDENTIFY"
tv_commands[11] = "CMD_REQUESTCONNECT"
tv_commands[13] = "CMD_DISCONNECT"
tv_commands[14] = "CMD_VNCDISCONNECT"
tv_commands[15] = "CMD_TVCONNECTIONFAILED"
tv_commands[16] = "CMD_PING"
tv_commands[17] = "CMD_PINGOK"
tv_commands[18] = "CMD_MASTERCOMMAND"
tv_commands[19] = "CMD_MASTERRESPONSE"
tv_commands[20] = "CMD_CHANGECONNECTION"
tv_commands[21] = "CMD_NOPARTNERCONNECT"
tv_commands[22] = "CMD_CONNECTTOWAITINGTHREAD"
tv_commands[23] = "CMD_SESSIONMODE"
tv_commands[24] = "CMD_REQUESTROUTINGSESSION"
tv_commands[25] = "CMD_TIMEOUT"
tv_commands[26] = "CMD_JAVACONNECT"
tv_commands[27] = "CMD_KEEPALIVEBEEP"
tv_commands[28] = "CMD_REQUESTKEEPALIVE"
tv_commands[29] = "CMD_MASTERCOMMAND_ENCRYPTED"
tv_commands[30] = "CMD_MASTERRESPONSE_ENCRYPTED"
tv_commands[31] = "CMD_REQUESTRECONNECT"
tv_commands[32] = "CMD_RECONNECTTOWAITINGTHREAD"
tv_commands[33] = "CMD_STARTLOGGING"
tv_commands[34] = "CMD_SERVERAVAILABLE"
tv_commands[35] = "CMD_KEEPALIVEREQUEST"
tv_commands[36] = "CMD_OK"
tv_commands[37] = "CMD_FAILED"
tv_commands[38] = "CMD_PING_PERFORMANCE"
tv_commands[39] = "CMD_PING_PERFORMANCE_RESPONSE"
tv_commands[40] = "CMD_REQUESTKEEPALIVE2"
tv_commands[41] = "CMD_DISCONNECT_SWITCHEDTOUDP"
tv_commands[42] = "CMD_SENDMODE_UDP"
tv_commands[43] = "CMD_KEEPALIVEREQUEST_ANSWER"
tv_commands[44] = "CMD_ROUTE_CMD_TO_CLIENT"
tv_commands[45] = "CMD_NEW_MASTERLOGIN"
tv_commands[46] = "CMD_BUDDY"
tv_commands[47] = "CMD_ACCEPTROUTINGSESSION"
tv_commands[48] = "CMD_NEW_MASTERLOGIN_ANSWER"
tv_commands[49] = "CMD_BUDDY_ENCRYPTED"
tv_commands[50] = "CMD_REQUEST_ROUTE_BUDDY"
tv_commands[51] = "CMD_CONTACT_OTHER_MASTER"
tv_commands[52] = "CMD_REQUEST_ROUTE_ENCRYPTED"
tv_commands[53] = "CMD_ENDSESSION"
tv_commands[54] = "CMD_SESSIONID"
tv_commands[55] = "CMD_RECONNECT_TO_SESSION"
tv_commands[56] = "CMD_RECONNECT_TO_SESSION_ANSWER"
tv_commands[57] = "CMD_MEETING_CONTROL"
tv_commands[58] = "CMD_CARRIER_SWITCH"
tv_commands[59] = "CMD_MEETING_AUTHENTICATION"
tv_commands[60] = "CMD_ROUTERCMD"
tv_commands[61] = "CMD_PARTNERRECONNECT"
tv_commands[62] = "CMD_CONGRESTION_CONTROL"
tv_commands[63] = "CMD_ACK"
tv_commands[70] = "CMD_UDPREQUESTCONNECT"
tv_commands[71] = "CMD_UDPPING"
tv_commands[72] = "CMD_UDPREQUESTCONNECT_VPN"
tv_commands[90] = "CMD_DATA"
tv_commands[91] = "CMD_DATA2"
tv_commands[92] = "CMD_DATA_ENCRYPTED"
tv_commands[93] = "CMD_REQUESTENCRYPTION"
tv_commands[94] = "CMD_CONFIRMENCRYPTION"
tv_commands[95] = "CMD_ENCRYPTIONREQUESTFAILED"
tv_commands[96] = "CMD_REQUESTNOENCRYPTION"
tv_commands[97] = "CMD_UDPFLOWCONTROL"
tv_commands[98] = "CMD_DATA3"
tv_commands[99] = "CMD_DATA3_ENCRYPTED"
tv_commands[100] = "CMD_DATA3_RESENDPACKETS"
tv_commands[101] = "CMD_DATA3_ACKPACKETS"
tv_commands[102] = "CMD_AUTH_CHALLENGE"
tv_commands[103] = "CMD_AUTH_RESPONSE"
tv_commands[104] = "CMD_AUTH_RESULT"
tv_commands[105] = "CMD_RIP_MESSAGES"
tv_commands[106] = "CMD_DATA4"
tv_commands[107] = "CMD_DATASTREAM"
tv_commands[108] = "CMD_UDPHEARTBEAT"
tv_commands[109] = "CMD_DATA_DIRECTED"
tv_commands[110] = "CMD_UDP_RESENDPACKETS"
tv_commands[111] = "CMD_UDP_ACKPACKETS"
tv_commands[112] = "CMD_UDP_PROTECTEDCOMMAND"
tv_commands[113] = "CMD_FLUSHSENDBUFFER"

local f_command = ProtoField.uint8("teamviewer.command", "Command", base.DEC, tv_commands)
local f_length = ProtoField.uint16("teamviewer.length", "Length", base.DEC)
local f_cmd2_length = ProtoField.uint32("teamviewer.length", "Length", base.DEC)
local f_data = ProtoField.bytes("teamviewer.data", "Data")

local f_command2_hdr_offset = ProtoField.uint32("teamviewer.header_offset", "Header offset", base.DEC)
local f_command2_hdr_cmd_class = ProtoField.uint32("teamviewer.header_cmd_class", "Header command class", base.DEC)
local f_command2_hdr_unknown = ProtoField.uint32("teamviewer.header_unknown", "Header unknown", base.DEC)
local f_command2_hdr_packet_id = ProtoField.uint32("teamviewer.header_packetid", "Header packet ID", base.DEC)
local f_command2_hdr_request_id = ProtoField.uint32("teamviewer.header_requestid", "Header request ID", base.DEC)

tv_proto.fields = {f_magic, f_command, f_length, f_cmd2_length, f_data, f_command2_hdr_offset, f_command2_hdr_unknown, f_command2_hdr_packet_id, f_command2_hdr_request_id, f_command2_hdr_cmd_class}

function tv_proto.dissector (buf, pkt, root)
  pkt.cols.protocol = tv_proto.name
  -- create subtree for tv_proto
  subtree = root:add(tv_proto, buf(0))
  -- add protocol fields to subtree
  local magic_item = subtree:add(f_magic, buf(0,2))
  local do_rotate = false
  if buf(0,2):uint() == 0x1130 then
  	pkt.private["is_cmd1"] = "false"
    magic_item:append_text(" command2")
  else
    pkt.private["is_cmd1"] = "true"
    magic_item:append_text(" command1")
  end
  
  subtree:add(f_command, buf(2,1))
  
  local data_length = 0
  local next_packet_offset = 0
  if pkt.private["is_cmd1"] == "true" then
  	subtree:add_le(f_length, buf(3,2))
    data_length = buf(3,2):le_uint()
    next_packet_offset = 5
  else
  	subtree:add_le(f_cmd2_length, buf(4,4))
    data_length = buf(4,4):le_uint()
    next_packet_offset = 24
  end
  
  if pkt.private["is_cmd1"] == "true" then
    data_tvb = buf(5, data_length):tvb()
    if buf(2,1):uint() ~= 46 then
      do_rotate = true
    end
  else
    subtree:add_le(f_command2_hdr_packet_id, buf(8,4))
    subtree:add_le(f_command2_hdr_request_id, buf(12,4))
    subtree:add_le(f_command2_hdr_cmd_class, buf(16,4))
    subtree:add_le(f_command2_hdr_offset, buf(20,4))
    data_tvb = buf(24, data_length):tvb()
    if buf(2,1):uint() == 93 or buf(2,1):uint() == 11 then
      do_rotate = true
    end
  end

  if do_rotate then
    -- do left rotation of 1
    local orig_data = data_tvb():bytes()
    local new_data = ByteArray.new()
    new_data:set_size(orig_data:len())
    if orig_data > 0 then 
    for x=0,orig_data:len()-2 do
      local newc = bit.band((bit.lshift(orig_data:get_index(x), 1) + bit.rshift(orig_data:get_index(x+1), 7)), 0xff)
      new_data:set_index(x,newc)
    end
    local newc = bit.band((bit.lshift(orig_data:get_index(orig_data:len()-1), 1) + bit.rshift(orig_data:get_index(0), 7)), 0xff)
    new_data:set_index(orig_data:len()-1,newc)
    data_tvb = ByteArray.tvb(new_data, "Decoded Data")
  end
end

  next_packet_offset = next_packet_offset+data_length
  local remaining_data = buf(next_packet_offset)

  local new_info = nil
  if tv_commands[buf(2,1):uint()] then
  	if pkt.private["is_cmd1"] == "true" then
      new_info = "TeamViewer v1 " .. tv_commands[buf(2,1):uint()] .. " Length " .. data_length
  	else
  		new_info = "TeamViewer v2 " .. tv_commands[buf(2,1):uint()] .. " Length " .. data_length
  	end
  else
  	if pkt.private["is_cmd1"] == "true" then
  		new_info = "TeamViewer v1 " .. buf(2,1):uint() .. " Length " .. data_length
  	else
  		new_info = "TeamViewer v2 " .. buf(2,1):uint() .. " Length " .. data_length
  	end
  end
  if pkt.private["did_change_info"] then
    pkt.cols.info:append(", " .. new_info)
  else
    pkt.cols.info = new_info
  end
  pkt.private["did_change_info"] = "1"

  if tv_commands[buf(2,1):uint()] then
  	tv_dissector_table:try(tv_commands[buf(2,1):uint()], data_tvb, pkt, subtree)
  else
    subtree:add(f_data, data_tvb:range())
  end
  
  if remaining_data:len() > 0 then
    tv_proto.dissector:call(remaining_data:tvb(), pkt, root)
  end


end

tcp_dissector_table = DissectorTable.get("tcp.port")
tcp_dissector_table:add(5938, tv_proto)
tv_dissector_table = DissectorTable.new("teamviewer.command", "TeamViewer Commands", ftypes.STRING)


ping_proto = Proto("teamviewer_ping","TeamViewer Ping")
local f_ping_from_id = ProtoField.uint32("teamviewer.from_id", "From ID", base.DEC)
ping_proto.fields = {f_ping_from_id}
function ping_proto.dissector (buf, pkt, root)
	root:add_le(f_ping_from_id, buf(0,4))
end
tv_dissector_table:add("CMD_PING", ping_proto)

mastercmd_proto = Proto("teamviewer_mastercmd","TeamViewer Master Command")
local f_mastercmd_config = ProtoField.string("teamviewer.mastercmd.config", "Configuration")
mastercmd_proto.fields = {f_mastercmd_config}
function mastercmd_proto.dissector (buf, pkt, root)
	root:add(f_mastercmd_config, buf(0))
end
tv_dissector_table:add("CMD_MASTERCOMMAND", mastercmd_proto)
tv_dissector_table:add("CMD_MASTERRESPONSE", mastercmd_proto)

identify_proto = Proto("teamviewer_identify","TeamViewer Identify")
local f_identify_from_id = ProtoField.uint32("teamviewer.from_id", "From ID", base.DEC)
local f_identify_license_type = ProtoField.uint32("teamviewer.license_type", "License Type", base.DEC)
local f_identify_gw_level = ProtoField.uint32("teamviewer.gw_level", "GW Level", base.DEC)
local f_static_unknown = ProtoField.uint32("teamviewer.static_unknown", "Unknown", base.DEC)
local f_supported_features = ProtoField.uint32("teamviewer.supported_features", "Supported Features", base.DEC)
identify_proto.fields = {f_identify_from_id, f_identify_gw_level, f_static_unknown, f_identify_license_type, f_supported_features}
function identify_proto.dissector (buf, pkt, root)
  root:add_le(f_identify_from_id, buf(0,4))
  root:add_le(f_identify_license_type, buf(4,4))
  root:add_le(f_identify_gw_level, buf(8,4))
  root:add_le(f_static_unknown, buf(12,4))
  root:add_le(f_static_unknown, buf(16,4))
  root:add_le(f_static_unknown, buf(20,4))
  root:add_le(f_supported_features, buf(24,4))
end
tv_dissector_table:add("CMD_IDENTIFY", identify_proto)


buddy_proto = Proto("teamviewer_buddy","TeamViewer Buddy")
local f_buddy_header_unknown_byte = ProtoField.uint32("teamviewer.header_unknown_byte", "Header Unknown", base.DEC, nil, 0x000000ff)
local f_buddy_header_unknown = ProtoField.uint32("teamviewer.header_unknown", "Header Unknown", base.DEC)
local f_buddy_header_from_id = ProtoField.uint32("teamviewer.header_unknown", "Header From ID", base.DEC)

param_names = {}
param_names[26] = "MessageLayer ID"

local f_buddy_command_type = ProtoField.uint8("teamviewer.param_cmd_type", "Command type", base.DEC)
local f_buddy_params_number_of_params = ProtoField.uint8("teamviewer.param_count", "Param Count", base.DEC)
local f_buddy_param_key = ProtoField.uint8("teamviewer.param_key", "Param Key", base.DEC)
local f_buddy_param_value_length = ProtoField.uint32("teamviewer.param_length", "Param Length", base.DEC)
local f_buddy_param_value = ProtoField.bytes("teamviewer.param_bytes", "Param Value")

buddy_proto.fields = {f_buddy_header_unknown_byte, f_buddy_header_unknown, f_buddy_header_from_id, f_buddy_command_type, f_buddy_params_number_of_params, f_buddy_param_key, f_buddy_param_value_length, f_buddy_param_value}
function buddy_proto.dissector (buf, pkt, root)
  param_off = 0
  if pkt.private["is_cmd1"] == "true" or buf(param_off,1):uint() == 0 then
    root:add_le(f_buddy_header_unknown_byte, buf(0,4))
    root:add_le(f_buddy_header_from_id, buf(4,4))
    root:add_le(f_buddy_header_unknown, buf(8,4))
    root:add_le(f_buddy_header_unknown, buf(12,4))
    root:add_le(f_buddy_header_unknown, buf(16,4))
    root:add_le(f_buddy_header_unknown, buf(20,4))
    param_off = 24
  end

  root:add(f_buddy_command_type, buf(param_off,1))
  param_off = param_off + 1
  root:add(f_buddy_params_number_of_params, buf(param_off,1))
  param_off = param_off + 1

  while param_off < buf:len() do 
    local key_item = root:add(f_buddy_param_key, buf(param_off,1))
    if param_names[buf(param_off,1):uint()] then
      key_item:append_text(" " .. param_names[buf(param_off,1):uint()])
    end
    param_off = param_off + 1
    local value_length = buf(param_off,4):le_uint()
    -- removed for clarity
    --root:add_le(f_buddy_param_value_length, buf(param_off,4))  
    param_off = param_off + 4
    root:add(f_buddy_param_value, buf(param_off, value_length))
    param_off = param_off + value_length
  end

end
tv_dissector_table:add("CMD_BUDDY", buddy_proto)

connection_request_proto = Proto("teamviewer_conn_req","TeamViewer Connection Request")
local f_conn_req_from_id = ProtoField.uint32("teamviewer.conn_req_from_id", "From ID", base.DEC)
local f_conn_req_dst_id = ProtoField.uint32("teamviewer.conn_req_dst_id", "Dest ID", base.DEC)
local f_conn_req_ip_string = ProtoField.string("teamviewer.req_ip", "Request IP")
local f_conn_req_connect_id = ProtoField.uint32("teamviewer.conn_req_connect_id", "Connection ID", base.DEC)
connection_request_proto.fields = {f_conn_req_from_id, f_conn_req_dst_id, f_conn_req_ip_string, f_conn_req_connect_id}
function connection_request_proto.dissector (buf, pkt, root)
  root:add_le(f_conn_req_from_id, buf(0,4))
  root:add_le(f_conn_req_dst_id, buf(4,4))
  root:add(f_conn_req_ip_string, buf(8,36))
  root:add_le(f_conn_req_connect_id, buf(44,4))
end
tv_dissector_table:add("CMD_REQUESTCONNECT", connection_request_proto)

data4_proto = Proto("teamviewer_data4","TeamViewer Data")
local f_data4_pkt_id = ProtoField.uint32("teamviewer.data4_pkt_id", "Packet ID", base.DEC)
local f_data4_response_id = ProtoField.uint32("teamviewer.data4_rsp_id", "Response ID", base.DEC)
local f_data4_is_encrypted = ProtoField.uint8("teamviewer.is_data_encrypted", "Is Encrypted", base.DEC)
local f_data4_unknown_byte = ProtoField.uint8("teamviewer.unknown_byte", "Unknown byte", base.DEC)
local f_data4_maybe_encrypted = ProtoField.bytes("teamviewer.maybe_encrypted", "Maybe encrypted")
data4_proto.fields = {f_data4_pkt_id, f_data4_response_id, f_data4_unknown_byte, f_data4_is_encrypted, f_data4_maybe_encrypted}
function data4_proto.dissector (buf, pkt, root)
  root:add_le(f_data4_pkt_id, buf(0,4))
  root:add_le(f_data4_response_id, buf(4,4))
  root:add_le(f_data4_is_encrypted, buf(8,1))
  root:add_le(f_data4_unknown_byte, buf(9,1))
  root:add_le(f_data4_maybe_encrypted, buf(12))
end
tv_dissector_table:add("CMD_DATA4", data4_proto)

req_enc_proto = Proto("teamviewer_request_encryption","TeamViewer Encryption Request")
local f_req_enc_pkt_id = ProtoField.uint32("teamviewer.req_enc_pkt_id", "Packet ID", base.DEC)
local f_req_enc_unknown = ProtoField.uint32("teamviewer.req_enc_unknown", "Unknown", base.DEC)
local f_req_enc_unknown_byte = ProtoField.uint8("teamviewer.req_enc_unknown_byte", "Unknown", base.DEC)

local f_req_enc_encrypted_keysize = ProtoField.uint32("teamviewer.encrypted_key_size", "Encrypted key size", base.DEC)
local f_req_enc_encrypted_key = ProtoField.bytes("teamviewer.encrypted_key", "Encrypted Key")

local f_req_enc_signature_size = ProtoField.uint32("teamviewer.signature_size", "Signature size", base.DEC)
local f_req_enc_signature = ProtoField.bytes("teamviewer.signature", "Signature")

req_enc_proto.fields = {f_req_enc_pkt_id, f_req_enc_unknown, f_req_enc_unknown_byte, f_req_enc_encrypted_key, f_req_enc_encrypted_keysize, f_req_enc_signature_size, f_req_enc_signature}
function req_enc_proto.dissector (buf, pkt, root)
  root:add_le(f_req_enc_pkt_id, buf(0,4))
  root:add_le(f_req_enc_unknown, buf(4,4))
  root:add_le(f_req_enc_unknown_byte, buf(8,1))
  root:add_le(f_req_enc_unknown_byte, buf(9,1))
  root:add_le(f_req_enc_encrypted_keysize, buf(12,4))
  local enc_size = buf(12,4):le_uint()
  root:add(f_req_enc_encrypted_key, buf(16,enc_size))
  local sig_size = buf(16+enc_size,4):le_uint()
  root:add_le(f_req_enc_signature_size, buf(16+enc_size,4))
  root:add(f_req_enc_signature, buf(20+enc_size,sig_size))
end
tv_dissector_table:add("CMD_REQUESTENCRYPTION", req_enc_proto)

session_mode_proto = Proto("teamviewer_session_mode","TeamViewer Session Mode")
local f_session_mode_value = ProtoField.uint32("teamviewer.session_mode_value", "Session value", base.DEC)
session_mode_proto.fields = {f_session_mode_value}
function session_mode_proto.dissector (buf, pkt, root)
  root:add_le(f_session_mode_value, buf(0,4))
  root:add_le(f_session_mode_value, buf(4,4))
  root:add_le(f_session_mode_value, buf(8,4))
  root:add_le(f_session_mode_value, buf(12,4))
  root:add_le(f_session_mode_value, buf(16,4))
  root:add_le(f_session_mode_value, buf(20,4))
  root:add_le(f_session_mode_value, buf(24,4))
end
tv_dissector_table:add("CMD_SESSIONMODE", session_mode_proto)