resource "aws_vpc" "main" {

 cidr_block = "10.0.0.0/16"

 

 tags = {

   Name = "Project YAT"

 }


}


resource "aws_subnet" "public_subnets" {

 count      = length(var.public_subnet_cidrs)

 vpc_id     = aws_vpc.main.id

 cidr_block = element(var.public_subnet_cidrs, count.index)

 

 tags = {

   Name = "Public Subnet ${count.index + 1}"

 }

}

 
resource "aws_internet_gateway" "gw" {

 vpc_id = aws_vpc.main.id

 

 tags = {

   Name = "Project YAT"

 }

}

variable "public_subnet_cidrs" {

 type        = list(string)

 description = "Public Subnet CIDR values"

 default     = ["10.0.1.0/24"]

}

resource "aws_route_table" "second_rt" {

 vpc_id = aws_vpc.main.id

 

 route {

   cidr_block = "0.0.0.0/0"

   gateway_id = aws_internet_gateway.gw.id

 }

 

 tags = {

   Name = "2nd Route Table"

 }

}

resource "aws_route_table_association" "public_subnet_asso" {

 count = length(var.public_subnet_cidrs)

 subnet_id      = element(aws_subnet.public_subnets[*].id, count.index)

 route_table_id = aws_route_table.second_rt.id

}


